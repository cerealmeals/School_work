#include "list.h"

Node nodes[LIST_MAX_NUM_NODES];
List heads[LIST_MAX_NUM_HEADS];

typedef struct Head_List Free_Heads;
struct Head_List{
    int count;
    List* current;
};

List free_nodes;
Free_Heads free_heads;
bool first = true;

Node* new_node(){
    //check if this is the last node if yes set last to null
    if(free_nodes.first == free_nodes.last){
        free_nodes.last = NULL;
    }
    //pick the first node in the list
    Node* to_return = free_nodes.first;
    //if the list was empty return a NULL pointer
    if(to_return == NULL){
        return to_return;
    }
    //if the list is not empty, reset the node
    to_return.next = NULL;
    //set the new first node and make sure it has no prev
    free_nodes.first = free_nodes.first->next
    free_nodes.first->prev = NULL;

    return to_return
}


List* List_create(){
    if(first){
        // initialize heads and list them in the free_heads header
        free_heads.count = LIST_MAX_NUM_HEADS;
        free_heads.current = heads[0];
        int i = 0
        for(; i < LIST_MAX_NUM_HEADS-1; i++){
            heads[i].count = 0;
            heads[i].current = NULL;
            heads[i].first = NULL;
            heads[i].last = NULL;
            heads[i].next = heads[i+1];
        }
        list[i].next = NULL;

        // initialize nodes and list them in the free_nodes header
        free_nodes.count = LIST_MAX_NUM_NODES;
        free_nodes.next = NULL;
        i = 1;
        nodes[i].next = nodes[i+1];
        nodes[i].prev = NULL;
        free_nodes.first = nodes[i];
        for(; i < LIST_MAX_NUM_NODES-1; i++){
            nodes[i].pointer = NULL;
            nodes[i].next = nodes[i+1];
            nodes[i].prev = nodes[i-1];

        }
        nodes[i].next = NULL;
        nodes[i].prev = nodes[i-1];
        free_nodes.last = nodes[i];

        first = false;
    }

    if(free_heads.count != 0){
        List* to_return = free_heads.current;
        free_heads.current = free_heads.current->next;
        free_heads.count--;
        return to_return;
    }
    else{
        return NULL;
    }
}

int List_count(List* pList){
    return pList->count;
}

void* List_first(List* pList){
    pList->current = pList->first;
    return pList->first->pointer;
}

void* List_last(List* pList){
    pList->current = pList->last;
    return pList->last->pointer;
}

void* List_next(List* pList){
    pList->current = pList->next;
    if(pList->current == NULL){
        pList->current = LIST_OOB_END;
    }
    return pList->next->pointer;
}

void* List_prev(List* pList){
    pList->current = pList->prev;
    if(pList->current == NULL){
        pList->current = LIST_OOB_START;
    }
    return pList->prev->pointer;
}

void* List_curr(List* pList){
    if(pList->current = LIST_OOB_END||pList->current = LIST_OOB_START){
        return NULL;
    }
    return pList->current->pointer;
}

int List_insert_after(List* pList, void* pItem){
    Node* new = new_node();
    if(new == NULL){
        return LIST_FAIL;
    }
    new->pointer = pItem;
    new->next = pList->current->next;
    new->prev = pList->current;
    pList->current->next = new;
    pList->current = new;

    return LIST_SUCCESS;
}

int List_insert_before(List* pList, void* pItem){
    
    Node* new = new_node();
    if(new == NULL){
        return LIST_FAIL;
    }
    new->pointer = pItem;
    new->next = pList->current;
    new->prev = pList->current->prev;
    pList->current->prev = new;
    pList->current = new;

    return LIST_SUCCESS;
}