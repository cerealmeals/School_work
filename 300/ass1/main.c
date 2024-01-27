#include "list.h"
#include "test.h"
#include <stdio.h>
#include <stdlib.h>

int main(){

    printf("hello world!\n");
    List* list1 = List_create();
    
    // int count = List_count(list1);
    // printf("number of nodes in list1: %d\n", count);

    int thing1 = 1, thing2 = 2, thing3 = 3, thing4 = 4;

    // {1}
    printf("append: 1\n");
    List_append(list1, &thing1);
    print_list(list1);
    
    // {1,2}
    printf("insert after: 2\n");
    List_insert_after(list1, &thing2);
    print_list(list1);

    // {1,3,2}
    printf("insert before: 3\n");
    List_insert_before(list1, &thing3);
    print_list(list1);

    // {4,1,3,2}
    printf("prepend: 4\n");
    List_prepend(list1, &thing4);
    print_list(list1);

    // // should print 2
    // int* print = List_last(list1);
    // printf("last item in list is: %d\n", (*print));


    // // should print 3
    // print = List_prev(list1);
    // printf("walk one backwards in list: %d\n", (*print));

    // // remove current should be 3
    // print = List_remove(list1);
    // printf("the current item was remove this item is: %d\n", (*print));
    List* list2 = List_create();

    for(int i = 0; i < 5; i++){
        int* to_insert = (int*)malloc(sizeof(int));
        *to_insert = i+5;
        List_prepend(list2, to_insert);
    }
    print_list(list2);

    // tests
    int answer;
    Test_List_create_empty();

    answer = 5;
    Test_List_count_normal(list2, answer);

    answer = 9;
    Test_List_first_normal(list2, answer);

    answer = 8;
    Test_List_next_normal(list2, answer);

    answer = 5;
    Test_List_last_normal(list2, answer);

    answer = 6;
    Test_List_prev_normal(list2, answer);
    
    Test_List_curr_normal(list2, answer);

    Test_List_remove_normal(list2, answer);

    answer = 5;
    Test_List_trim_normal(list2, answer);

    FREE_FN free_er = free_int;
    Test_List_free_normal(list2, free_er);

    Test_List_create_normal();

    list2 = List_create();

    answer = 0;
    Test_List_count_empty(list2, answer);

    Test_List_first_empty(list2, answer);

    Test_List_last_empty(list2, answer);

    Test_List_next_empty(list2, answer);

    Test_List_pre_empty(list2, answer);

    Test_List_curr_empty(list2, answer);

    


    return 0;
}