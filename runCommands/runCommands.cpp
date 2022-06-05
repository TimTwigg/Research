// updated 5 June 2022
// C++ module to run commands by simulating keyboard input

#include <string>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <map>
#include <time.h>

bool write(char c) {
    // Sam's answer at
    // https://stackoverflow.com/questions/2167156/sendinput-isnt-sending-the-correct-shifted-characters
    
    INPUT input[ 2 ];

    input[0].type = INPUT_KEYBOARD;
    input[0].ki.wVk = 0;
    input[0].ki.wScan = c;
    input[0].ki.dwFlags = KEYEVENTF_UNICODE;
    input[0].ki.time = 0;
    input[0].ki.dwExtraInfo = 0;

    input[1].type = INPUT_KEYBOARD;
    input[1].ki.wVk = 0;
    input[1].ki.wScan = c;
    input[1].ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;
    input[1].ki.time = 0;
    input[1].ki.dwExtraInfo = 0;

    SendInput(2, input, sizeof(INPUT));
    return true;
}

void enter() {
    INPUT ip;
    ip.type = INPUT_KEYBOARD;
    ip.ki.time = 0;
    ip.ki.dwFlags = KEYEVENTF_UNICODE;
    ip.ki.wScan = VK_RETURN;
    ip.ki.wVk = 0;
    ip.ki.dwExtraInfo = 0;
    SendInput(1, &ip, sizeof(INPUT));
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

    Sleep(2000);

    while (in) {
        std::string command;
        std::getline(in, command);
        if (command.size() < 1) break;

        // this method of writing individual characters is reliable (with the sleep) but slow
        write('\\');
        for (char c : command) {
            write(c);
            Sleep(1); // without this is works nicely for a while then goes mad
        }
        enter();
    }

    std::cout << "complete" << std::endl;

    return 0;
}