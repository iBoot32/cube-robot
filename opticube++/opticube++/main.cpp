#include "cubestringcalc.h"
#include <vector>
#include <iostream>
#include <algorithm>
#include <set>
#include <chrono>
using namespace std;

void print_str(char*, std::string, const int, const int);
void check(std::string str[]);

int main(int argc, char *argv[])
{
    auto begin = std::chrono::high_resolution_clock::now();
    calc(argv, argc);

    int length = 4;
    char str[] = { 'A', 'B', 'C',   'D', 'E', 'F',   'G', 'H', 'I',   'J', 'K', 'L',   'M', 'N', 'O',   'P', 'Q', 'R'};
    int n = sizeof str;

    print_str(str, "", sizeof(str), length);
    auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::high_resolution_clock::now() - begin);
    printf("Time elapsed: %.4fms\n", elapsed.count() * 1e-6);
}


void print_str(char str[], std::string prefix, const int n, const int length)
{
    if (length != 1)
    {
        for (int i = 0; i < n; i++)
        {
            print_str(str, prefix + str[i], n, length - 1);
        }
    }
    else
    {
        for (int j = 0; j < n; j++)
        {
            check(prefix + str[j]);
        }
    }
}

void check(std::string str[])
{

}
