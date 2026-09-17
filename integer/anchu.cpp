#include<iostream>
using namespace std;
int main()
{
int n,a;
n=583258;
a=n%10;
if(a>7)
{
    cout<<"The first largest digit:"<<a;
}
else
{
    cout<<"The second largest digit:"<<a;
}
return 0;
}