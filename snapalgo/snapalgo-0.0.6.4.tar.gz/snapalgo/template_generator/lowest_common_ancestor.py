#lowest common ancestor template
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
def expand(root,nodes):
    if root == None:
        return None
    
    elif root in nodes:
        return root
    
    left = expand(root.left,nodes)
    right = expand(root.right,nodes)
    
    if left and right:
        return root
    
    elif left:
        return left
    elif right:
        return right

return expand(root,nodes)