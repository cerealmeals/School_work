#include "list.h"
#include "test.h"

#include <stdio.h>

void print_list(List* plist);

int main(){

    printf("hello world!\n");
    List* list1 = List_create();
    
    int count = List_count(list1);
    printf("number of nodes in list1: %d\n", count);

    int thing1 = 1, thing2 = 2, thing3 = 3, 
        thing4 = 4;
    
    int check;

    // {1}
    printf("append: 1\n");
    check = List_append(list1, &thing1);
    print_list();

    // {1,2}
    printf("insert after: 2\n");
    check = List_insert_after(list1, &thing2);
    print_list();

    // {1,3,2}
    printf("insert before: 3\n");
    check = List_insert_before(list1, &thing3);
    print_list();

    // {4,1,3,2}
    printf("prepend: 4\n");
    check = List_prepend(list1, &thing4);
    print_list(list1);

    // should print 2
    int* print = List_last(list1);
    printf("last item in list is: %d\n", (&print));


    // should print 3
    print = list_prev(list1);
    printf("walk one backwards in list: %d\n", (&print));

    // remove current should be 3
    print = List_remove(list1);
    printf("the current item was remove this item is: %d\n", (&print));

    // 

    List* list2 = List_create();

    for(int i = 0; i < 5; i++){
        int to_insert = (*int)malloc(4);
        List_prepend(list2, &to_insert);
    }
    print_list(list2);



    return 0;
}