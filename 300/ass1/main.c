#include "list.h"

#include <stdio.h>

int main(){

    printf("hello world!\n");
    List* list1 = List_create();
    
    int count = List_count(list1);

    printf("number of nodes in list1: %d\n", count);

    int thing1 = 1, thing2 = 2, thing3 = 3, 
        thing4 = 4, thing5 = 5, thing6 = 6, 
        thing7 = 7, thing8 = 8, thing9 = 9;
    
    int check;
    printf("address of thing1: %p\n", &thing1);

    check = List_append(list1, &thing1);

    printf("number of nodes in list1: %d\n", count);
    return 0;
}
