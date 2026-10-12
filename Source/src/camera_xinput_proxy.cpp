#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <Xinput.h>
#include <algorithm>
#include <chrono>
#include <climits>
#include <cmath>
#include <cstdarg>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <cwchar>
#include <mutex>
#include <string>

namespace {
using XInputGetStateFn = DWORD (WINAPI *)(DWORD, XINPUT_STATE *);
using XInputSetStateFn = DWORD (WINAPI *)(DWORD, XINPUT_VIBRATION *);
using XInputGetCapabilitiesFn = DWORD (WINAPI *)(DWORD, DWORD, XINPUT_CAPABILITIES *);

HMODULE g_module = nullptr;
HMODULE g_systemXinput = nullptr;
XInputGetStateFn g_getState = nullptr;
XInputSetStateFn g_setState = nullptr;
XInputGetCapabilitiesFn g_getCapabilities = nullptr;
std::once_flag g_initOnce;
std::once_flag g_logSampleOnce;
float g_xExponent = 0.70f;
float g_yExponent = 0.70f;
float g_xGain = 1.0f;
float g_yGain = 1.0f;
std::wstring SiblingPath(const wchar_t *filename) {
    wchar_t modulePath[MAX_PATH]{};
    if (!g_module || !GetModuleFileNameW(g_module, modulePath, MAX_PATH)) return {};
    std::wstring path(modulePath);
    const size_t slash = path.find_last_of(L"\\/");
    path.resize(slash == std::wstring::npos ? 0 : slash + 1);
    path += filename;
    return path;
}

void Log(const char *format, ...) {
    char message[512]{};
    va_list args;
    va_start(args, format);
    vsnprintf(message, sizeof(message), format, args);
    va_end(args);
    const std::wstring path = SiblingPath(L"camera_axis_fix.log");
    HANDLE file = path.empty() ? INVALID_HANDLE_VALUE : CreateFileW(
        path.c_str(), FILE_APPEND_DATA, FILE_SHARE_READ | FILE_SHARE_WRITE,
        nullptr, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);
    if (file != INVALID_HANDLE_VALUE) {
        DWORD written = 0;
        WriteFile(file, message, static_cast<DWORD>(strlen(message)), &written, nullptr);
        WriteFile(file, "\r\n", 2, &written, nullptr);
        CloseHandle(file);
    }
    OutputDebugStringA(message);
}

float ReadIniFloat(const std::wstring &ini, const wchar_t *key, float fallback,
                   float minimum, float maximum) {
    wchar_t value[32]{};
    GetPrivateProfileStringW(L"Camera", key, L"", value, ARRAYSIZE(value), ini.c_str());
    if (!value[0]) return fallback;
    wchar_t *end = nullptr;
    const float parsed = wcstof(value, &end);
    return end != value && std::isfinite(parsed)
        ? std::clamp(parsed, minimum, maximum) : fallback;
}

SHORT ApplyCurve(SHORT input, float exponent, float gain) {
    constexpr int deadzone = XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE;
    const int raw = input;
    const int magnitude = std::abs(raw);
    if (magnitude <= deadzone) return 0;
    const float t = static_cast<float>(magnitude - deadzone) /
                    static_cast<float>(SHRT_MAX - deadzone);
    const float curved = std::pow(std::clamp(t, 0.0f, 1.0f), exponent);
    const int outputMagnitude = (std::min)(SHRT_MAX, deadzone + static_cast<int>(std::lround(
        curved * gain * static_cast<float>(SHRT_MAX - deadzone))));
    const int signedOutput = raw < 0 ? -outputMagnitude : outputMagnitude;
    return static_cast<SHORT>(std::clamp(signedOutput, -SHRT_MAX, SHRT_MAX));
}

bool Initialize() {
    std::call_once(g_initOnce, [] {
        const std::wstring ini = SiblingPath(L"camera_axis_fix.ini");
        g_xExponent = ReadIniFloat(ini, L"RightStickXExponent", 0.70f, 0.35f, 1.0f);
        g_yExponent = ReadIniFloat(ini, L"RightStickYExponent", 0.70f, 0.35f, 1.0f);
        g_xGain = ReadIniFloat(ini, L"RightStickXGain", 1.0f, 0.25f, 4.0f);
        g_yGain = ReadIniFloat(ini, L"RightStickYGain", 1.0f, 0.25f, 4.0f);
        wchar_t systemDirectory[MAX_PATH]{};
        const UINT length = GetSystemDirectoryW(systemDirectory, MAX_PATH);
        if (!length || length >= MAX_PATH) return;
        std::wstring path(systemDirectory);
        path += L"\\xinput1_3.dll";
        g_systemXinput = LoadLibraryW(path.c_str());
        if (!g_systemXinput) return;
        g_getState = reinterpret_cast<XInputGetStateFn>(
            GetProcAddress(g_systemXinput, "XInputGetState"));
        g_setState = reinterpret_cast<XInputSetStateFn>(
            GetProcAddress(g_systemXinput, "XInputSetState"));
        g_getCapabilities = reinterpret_cast<XInputGetCapabilitiesFn>(
            GetProcAddress(g_systemXinput, "XInputGetCapabilities"));
        Log("XInput proxy active; system=%ls; gain X/Y=%.2f/%.2f exponent X/Y=%.2f/%.2f", path.c_str(), g_xGain, g_yGain, g_xExponent, g_yExponent);
        if (!g_getState || !g_setState || !g_getCapabilities)
            Log("XInput forwarding export missing: GetState=%d SetState=%d GetCapabilities=%d",
                g_getState != nullptr, g_setState != nullptr, g_getCapabilities != nullptr);
    });
    return g_getState && g_setState && g_getCapabilities;
}
}

BOOL WINAPI DllMain(HINSTANCE instance, DWORD reason, LPVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        g_module = instance;
        DisableThreadLibraryCalls(instance);
    }
    return TRUE;
}

extern "C" DWORD WINAPI ProxyXInputGetState(DWORD userIndex, XINPUT_STATE *state) {
    if (!Initialize()) return ERROR_DEVICE_NOT_CONNECTED;
    const DWORD result = g_getState(userIndex, state);
    if (result == ERROR_SUCCESS && state) {
        const SHORT originalX = state->Gamepad.sThumbRX;
        const SHORT originalY = state->Gamepad.sThumbRY;
            const SHORT adjustedX = ApplyCurve(originalX, g_xExponent, g_xGain);
            const SHORT adjustedY = ApplyCurve(originalY, g_yExponent, g_yGain);
            state->Gamepad.sThumbRX = adjustedX;
            state->Gamepad.sThumbRY = adjustedY;
            if (std::abs(static_cast<int>(originalX)) > XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE ||
                std::abs(static_cast<int>(originalY)) > XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE) {
                std::call_once(g_logSampleOnce, [=] {
                    Log("XInputGetState user=%lu; raw RX/RY=%d/%d; adjusted RX/RY=%d/%d",
                        userIndex, originalX, originalY, adjustedX, adjustedY);
                });
            }
    }
    return result;
}

extern "C" DWORD WINAPI ProxyXInputSetState(DWORD userIndex, XINPUT_VIBRATION *vibration) {
    if (!Initialize()) return ERROR_DEVICE_NOT_CONNECTED;
    return g_setState(userIndex, vibration);
}

extern "C" DWORD WINAPI ProxyXInputGetCapabilities(DWORD userIndex, DWORD flags,
                                                     XINPUT_CAPABILITIES *capabilities) {
    if (!Initialize()) return ERROR_DEVICE_NOT_CONNECTED;
    return g_getCapabilities(userIndex, flags, capabilities);
}
