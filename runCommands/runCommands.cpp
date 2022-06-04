// updated 3 June 2022
// C++ module to run commands by simulating keyboard input

#include <string>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <conio.h>

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

    char c = getch();

    while (in) {
        std::string command;
        std::getline(in, command);
        
        // replace this with simulating keybaord rather than sending to cout
        std::cout << command << std::endl;
        INPUT ip;
        ip.type = INPUT_KEYBOARD;
        ip.ki.time = 0;
        ip.ki.dwExtraInfo = 0;

        // need a map to get the right code, then press, then release
        // gonna need to loop through each string
    }

    return 0;
}