from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def reverse_postorder_recursive(root: Optional[TreeNode]) -> List[int]:

    result = []
    
    def traverse(node):
        if not node:
            return
        traverse(node.right) 
        traverse(node.left)  
        result.append(node.val) 
        
    traverse(root)
    return result

def reverse_postorder_iterative(root: Optional[TreeNode]) -> List[int]:

    if not root:
        return []
    
    result = []
    stack = [root]
    

    while stack:
        node = stack.pop()
        result.append(node.val)
        

        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
            
    return result[::-1]

def build_tree(depth: int, current_val: int) -> Optional[TreeNode]:
   
    if depth == 0:
        return None
    root = TreeNode(current_val)
    
    root.left = build_tree(depth - 1, current_val * 2)
    root.right = build_tree(depth - 1, current_val * 2 + 1)
    return root

if __name__ == "__main__":

    tree = build_tree(3, 1)
    
    res_rec = reverse_postorder_recursive(tree)
    res_iter = reverse_postorder_iterative(tree)
    
    print(f"Рекурсивный обход: {res_rec}")
    print(f"Итеративный обход: {res_iter}")
    
    if res_rec == res_iter:
        print("Результаты идентичны!")
    else:
        print("Ошибка: результаты различаются.")