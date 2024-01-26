#include "list.h"

void free_int(void* pItem) {
  // cast pItem to a char pointer
  int* i = (int*) pItem;
  // free the memory allocated for the string
  free(i);
}

void print_list(List* plist){
    int* print = List_first(plist);
    printf("List contains: %d\n", (*print));
    bool flag = true;
    while(flag){
        print = List_next(plist);
        if(print != 0){
            printf(" %d\n", (*print));
        }
        else{
            flag = false;
        }
    }
    printf("\n");
}

void Test_List_create_normal(){
    List* list = List_create();
    assert(list != 0);
    FREE_FN delete = free_int;
    List_free(list, delete);
}

void Test_List_create_empty(){
    List* list = List_create();
    assert(list == 0);
    FREE_FN delete = free_int;
    List_free(list, delete);
}

void Test_List_count_normal(List* plist, int answer){
    int guess = List_count(plist);
    assert(guess == answer);
}

void Test_List_count_empty(List* plist, int answer){
    int guess = List_count(plist);
    assert(guess == answer); 
}

void Test_List_first_normal(List* plist, int answer{
    int* guess = List_first(plist);
    assert(&guess == answer);
}

void Test_List_first_empty(List* plist, int answer){
    int* guess = List_first(plist);
    assert(&guess == answer);
}

void Test_List_last_normal(List* plist, int answer){
    int* guess = List_last(plist);
    assert(&guess == answer);
}

void Test_List_last_empty(List* plist, int answer){
    int* guess = List_last(plist);
    assert(&guess == answer);
}

void Test_List_next_normal(List* plist, int answer){
    int* guess = List_next(plist);
    assert(&guess == answer);
}

void Test_List_next_empty(List* plist, int answer){
    int* guess = List_next(plist);
    assert(&guess == answer);
}

void Test_List_prev_normal(List* plist, int answer){
    int* guess = List_prev(plist);
    assert(&guess == answer);
}

void Test_List_prev_empty(List* plist, int answer){
    int* guess = List_prev(plist);
    assert(&guess == answer);
}

void Test_List_curr_normal(List* plist, int answer){
    int* guess = List_curr(plist);
    assert(&guess == answer);
}

void Test_List_curr_empty(List* plist, int answer){
    int* guess = List_curr(plist);
    assert(&guess == answer);
}

void Test_List_curr_OOB_end(List* plist, int answer){
    int* guess = List_curr(plist);
    assert(&guess == answer);
}

void Test_List_curr_OOB_start(List* plist, int answer){
    int* guess = List_curr(plist);
    assert(&guess == answer);
}

void Test_List_insert_after_normal(List* plist, int answer){
    int check = List_insert_after(plist, answer);
    assert(check == 0);
    print_list(plist);
}

void Test_List_insert_after_empty(List* plist, int answer){
    int check = List_insert_after(plist, answer);
    assert(check == 0);
    print_list(plist);
}

void Test_List_insert_after_none(List* plist, int answer){
    int check = List_insert_after(plist, answer);
    assert(check == -1);
}

void Test_List_insert_before_normal(List* plist, int answer){
    int check = List_insert_before(plist, answer);
    assert(check == 0);
    print_list(plist);
}

void Test_List_insert_before_empty(List* plist, int answer){
    int check = List_insert_before(plist, answer);
    assert(check == 0);
    print_list(plist);
}

void Test_List_insert_before_none(List* plist, int answer){
    int check = List_insert_before(plist, answer);
    assert(check == -1);
}

void Test_List_append_normal(List* plist, int answer){
    int check = List_append(plist, answer);
    assert(check == 0);
    print_list(plist);
}

void Test_List_append_empty(List* plist, int answer){

}

void Test_List_prepend_normal(List* plist, int answer);

void Test_List_prepend_empty(List* plist, int answer);

void Test_List_remove_normal(List* plist);

void Test_List_remove_empty(List* plist);

void Test_List_remove_last(List* plist);

void Test_List_trim_normal(List* plist);

void Test_List_trim_empty(List* plist);

void Test_List_trim_last(List* plist);

void Test_List_concat_normal(List* plist1, List8 plist2);

void Test_List_concat_empty_list1(List* plist1, List8 plist2);

void Test_List_concat_empty_list2(List* plist1, List8 plist2);

void Test_List_free_normal(List* plist, FREE_FN pItemFreeFn){
    List_free(plist, pItemFreeFn);
    assert(plist == 0);
}

void Test_List_free_empty(List* plist, FREE_FN pItemFreeFn){
    List_free(plist, pItemFreeFn);
    assert(plist == 0);
}

void Test_List_search_normal(List* pList, COMPARATOR_FN pComparator, void* pComparisonArg);

void Test_List_search_OOB_start(List* pList, COMPARATOR_FN pComparator, void* pComparisonArg);

void Test_List_search_OOB_end(List* pList, COMPARATOR_FN pComparator, void* pComparisonArg);

void Test_List_search_empty(List* pList, COMPARATOR_FN pComparator, void* pComparisonArg);