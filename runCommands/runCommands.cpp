// updated 9 October 2023
// C++ module to run commands by simulating keyboard input

#include <string>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <cassert>
#include <time.h>

#ifndef ESCAPE
#define ESCAPE 0x01
#endif

#ifndef ENTER
#define ENTER 0x1c
#endif

#ifndef SLASH
#define SLASH 0x35
#endif

// Append a character to the input vector
void append(char c, std::vector<INPUT>& v) {
    // Adapted from Sam's answer at
    // https://stackoverflow.com/questions/2167156/sendinput-isnt-sending-the-correct-shifted-characters
    
    // key down
    INPUT input;
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = 0;
    input.ki.wScan = c;
    input.ki.dwFlags = KEYEVENTF_UNICODE;
    input.ki.time = 0;
    input.ki.dwExtraInfo = 0;
    v.push_back(input);

    // key up
    INPUT input2;
    input2.type = INPUT_KEYBOARD;
    input2.ki.wVk = 0;
    input2.ki.wScan = c;
    input2.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;
    input2.ki.time = 0;
    input2.ki.dwExtraInfo = 0;
    v.push_back(input2);
}

// Press the key designated by code
void press(int code) {
    INPUT KEY_B;

	KEY_B.type = INPUT_KEYBOARD;
	KEY_B.ki.time = 0;
	KEY_B.ki.wVk = 0;
	KEY_B.ki.dwExtraInfo = 0;
	KEY_B.ki.dwFlags = KEYEVENTF_SCANCODE;
	KEY_B.ki.wScan = code;

	SendInput(1, &KEY_B, sizeof(INPUT));
	KEY_B.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
	SendInput(1, &KEY_B, sizeof(INPUT));
}

// run by calling exe with single arg of the filename to run
int main(int argc, char** argv) {
    // arguments should be [thisFileName, fileNameToRun]
    if (argc != 2) {
        std::cout << "Invalid argument count: " << argc << std::endl;
        return 1;
    }
    std::string filename = argv[1];

    // verify that the file exists
    std::ifstream in{filename};
    if (!in) {
        std::cout << "File not Found: " << filename << std::endl;
        return 1;
    }

    // assumes the minecraft is loaded into the world, with escape then pressed to focus another app
    press(ESCAPE);

    // Pause before beginning to run commands
    Sleep(1000);

    while (in) {
        std::vector<INPUT> v;
        std::string command;
        std::getline(in, command);
        if (command.size() < 1) break;

        // add characters of command to Input vector
        for (char c : command) {
            append(c, v);
        }

        Sleep(25); // pause
        press(SLASH); // open command line
        Sleep(100); // wait for command line to open
        SendInput(v.size(), v.data(), sizeof(INPUT)); // print command
        Sleep(100); // wait for command to print
        press(ENTER); // press enter to run command
    }

    return 0;
}