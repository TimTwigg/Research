// updated 6 June 2022
// C++ module to run commands by simulating keyboard input

#include <string>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <cassert>
#include <time.h>

void append(char c, std::vector<INPUT>& v) {
    // Adapted from Sam's answer at
    // https://stackoverflow.com/questions/2167156/sendinput-isnt-sending-the-correct-shifted-characters
    
    INPUT input;
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = 0;
    input.ki.wScan = c;
    input.ki.dwFlags = KEYEVENTF_UNICODE;
    input.ki.time = 0;
    input.ki.dwExtraInfo = 0;
    v.push_back(input);

    INPUT input2;
    input2.type = INPUT_KEYBOARD;
    input2.ki.wVk = 0;
    input2.ki.wScan = c;
    input2.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;
    input2.ki.time = 0;
    input2.ki.dwExtraInfo = 0;
    v.push_back(input2);
}

void enter(std::vector<INPUT>& v) {
    INPUT ip;
    ip.type = INPUT_KEYBOARD;
    ip.ki.time = 0;
    ip.ki.dwFlags = KEYEVENTF_UNICODE;
    ip.ki.wScan = VK_RETURN;
    ip.ki.wVk = 0;
    ip.ki.dwExtraInfo = 0;
    v.push_back(ip);
}

// run by calling exe with single arg of the filename to run
int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "Invalid argument count: " << argc << std::endl;
        return 1;
    }
    std::string filename = argv[1];

    std::ifstream in{filename};
    if (!in) {
        std::cout << "File not Found: " << filename << std::endl;
        return 1;
    }

    while (in) {
        std::vector<INPUT> v;
        std::string command;
        std::getline(in, command);
        if (command.size() < 1) break;

        append('/', v);
        for (char c : command) {
            append(c, v);
        }
        enter(v);
        SendInput(v.size(), v.data(), sizeof(INPUT));
        Sleep(50);
    }

    return 0;
}