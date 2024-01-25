#include "list.h"

#include <stdio.h>

void print_list(List* plist);

int main(){

    printf("hello world!\n");
    List* list1 = List_create();
    
    int count = List_count(list1);
    printf("number of nodes in list1: %d\n", count);

    int thing1 = 1, thing2 = 2, thing3 = 3, 
        thing4 = 4, thing5 = 5, thing6 = 6, 
        thing7 = 7, thing8 = 8, thing9 = 9;
    
    int check;

    // {1}
    check = List_append(list1, &thing1);
    if(check == 0){
        printf("List_append worked!\n");
    }
    count = List_count(list1);
    printf("number of nodes in list1: %d\n", count);

    // {1,2}
    check = List_insert_after(list1, &thing2);
    if(check == 0){
        printf("List_insert_after worked!\n");
    }
    count = List_count(list1);
    printf("number of nodes in list1: %d\n", count);

    // {1,3,2}
    check = List_insert_before(list1, &thing3);
    if(check == 0){
        printf("List_insert_before worked!\n");
    }
    count = List_count(list1);
    printf("number of nodes in list1: %d\n", count);

    // {4,1,3,2}
    check = List_prepend(list1, &thing4);
    if(check == 0){
        printf("List_prepend worked!\n");
    }
    count = List_count(list1);
    printf("number of nodes in list1: %d\n", count);

    print_list(list1);

    List* list2 = List_create();


    return 0;
}


void print_list(List* plist){
    int* print = List_first(plist);
    printf("List contains: %d\n", (*print));
    while(plist->current != 0){
        print = List_next(plist);
        printf(" %d\n", (*print));
    }
    printf("\n");
}