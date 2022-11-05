def bubble_sort(nums):
    
    for x in range(len(nums)):
        for y in range(len(nums)-x-1):
            swapped = False
            if nums[y] > nums[y+1]:
                nums[y],nums[y+1] = nums[y+1],nums[y]
                swapped = True
                
            if swapped == False:
                break
                
    return nums