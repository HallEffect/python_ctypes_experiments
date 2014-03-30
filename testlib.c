#include <stdio.h>

struct foo
{
	int x;
	float y;
	int mas[10];
	int* p;
};

int test(int x)
{
	return x;
}

int* bar(struct foo str, int* pointer_pamameter)
{	
	int k=*pointer_pamameter;
	k++;
	return &k;
}

