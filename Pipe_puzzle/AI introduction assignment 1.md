---
type:
  - Daily
tags:
  - AI
  - Game
  - Pygame
  - BTL
  - Pipe
  - Vietnamese
published: true
folder: Daily
---
# Blind search

Đối với giải thuật blind search, nhóm chọn depth first search để hiện thực cho game Pipe puzzle này. Nhóm sử dụng cấu trúc dữ liệu stack để lưu và duyệt các trạng thái (state) theo chiều sâu sau mỗi lần lấy ra đỉnh stack. Một state trong giải thuật depth first search sẽ được định nghĩa như sau:

```python
list_of_tiles = [Tile(), ...]
list_of_steps = [(x, y, step)]
state = (list_of_tiles, list_of_steps)
```

trong đó trạng thái của một ô (Tile) gồm có hình dạng của ống nước (chữ L, chữ T, ...), ống đó có nước đi qua hay không, ô đó có phải nguồn nước không. Các bước (step) để đến được state này sẽ bao gồm các hành động mà người chơi có thể làm, ví dụ như xoay ngược chiều kim đồng hồ ô có tọa độ (1, 1), xoay theo chiều kim đồng hồ ô có tọa độ (0,2) hay xoay 2 lần theo chiều kim đồng hồ ô (0, 0). Sẽ có tất cả là ba hành động có thể làm để xoay được ô chứa ống nước thành các trạng thái khác nhau so với trạng thái ban đầu. Để sinh state mới thì ta sẽ áp dụng lần lượt 3 hành động này lần lượt vào mỗi ô, như vậy vậy game size 3x3 thì ta sinh được 3 x 3 x 3 = 27 state mới. Cứ mỗi lần sinh state mới thì các step mới sẽ được thêm vào state mới đó. Nói cách khác list_of_steps của goal state sẽ là lời giải cho bài toán Pipe puzzle.

Depth first search sẽ duyệt qua các state này trong stack và đánh giá state trong vòng lặp while cho đến khi tìm thấy được goal state thì ngừng. Một state sẽ được xem là goal state nếu tất cả các ô trong game đều có nước đi qua và không có ống nước nào là không được kết nối.

Dưới đây là mã giả cho bài toán (được hiện thực trong hàm blind_search của file core.py):

```python
stack = []
visited = [chosen_state]

while not reach_goal(chosen_state):
	# loop qua từng ô có trong game để xoay nó qua bên phải (clockwise)
	for tile in chosen_state[0]:
		new_list_of_tiles = tile.rotate_clockwise()
		new_list_of_steps = chosen_state[1].append(tile.x, tile.y, 'right')
		new_state = (new_list_of_tiles, new_list_of_steps)

		# Nếu new_state chưa được visit thì đưa nó vào trong stack
		if not is_visited(new_state, visited):
			stack.append(new_state)
	
	# loop qua từng ô trong game để xoay nó qua bên trái (anti clockwise)
	for tile in chosen_state[0]:
		new_list_of_tiles = tile.rotate_anti_clockwise()
		new_list_of_steps = chosen_state[1].append(tile.x, tile.y, 'left')
		new_state = (new_list_of_tiles, new_list_of_steps)

		# Nếu new_state chưa được visit thì đưa nó vào trong stack
		if not is_visited(new_state, visited):
			stack.append(new_state)

	# loop qua từng ô trong game để xoay nó hai lần	
	for tile in chosen_state[0]:
		new_list_of_tiles = tile.rotate_anti_clockwise()
		new_list_of_tiles = tile.rotate__anti_clockwise()
		new_list_of_steps = chosen_state[1].append(tile.x, tile.y, 'left left')
		new_state = (new_list_of_tiles, new_list_of_steps)

		# Nếu new_state chưa được visit thì đưa nó vào trong stack
		if not is_visited(new_state, visited):
			stack.append(new_state)

	chosen_state = stack.pop()
	visited.append(chosen_state)
	if len(stack) == 0:
		break
	
```

Lưu ý thêm rằng do áp dụng blind_search cho bài toán Pipe puzzle chỉ có một goal state nên việc tìm ra lời giải là rất khó khăn. Đối với các game 4x4 và 5x5 đều đã được chạy giải thử rất lâu nhưng vẫn không thể tìm ra được lời giải. Vì vậy nên nhóm chỉ hiện thực depth first search cho bài toán 3x3 với điều chỉnh dễ dàng hơn về độ khó.

Các khái niệm về ô (Tile), các hành động áp dụng được với một ô và step sẽ tiếp tục được sử dụng trong thuật toán A* phía dưới.

#  Heuristic search

Đối với heuristic, nhóm chọn giải thuật A* để hiện thực. Giải thuật A* sẽ tiếp tục sử dụng list visited để lưu trữ các state đã đi qua và một list khác là checking_states để lưu lại các state đang xét nhằm lấy ra state tốt nhất tại thời điểm xét đó.

State của A* search ngoài hai thành phần list_of_tiles và list_of_steps như của depth first search thì còn thêm vào hai thành phần mới mang đặc trưng của giải thuật này là greedy cost (hn) và uniform cost (gn).

```python
list_of_tiles = [Tile(), ...]
list_of_steps = [(x, y, step)]
hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3
gn = 0
state = (list_of_tiles, hn, list_of_steps, gn)
```

trong đó:
- gn: số bước thực hiện để đến được state hiện tại, ở đây xoay một ô 2 lần liên tiếp cũng được tính là một bước. Qua mỗi state gn sẽ được cộng lên một so với state trước đó.

- hn: được tính bằng công thức sau đây
```python
hn = (số đầu ống nước bị hở) / 2 + (số ống không có nước) + (số đầu ống nước hướng vào tường) * 5 + (số đầu ống deadend hướng vào nhau) * 5 + (số vòng lặp ống) * 3
```

với 1/2, 1, 5, 5, 3 lần lượt là các hệ số để thể hiện mức độ quan trọng. Hệ số càng cao thì cost tại đó càng lớn, như việc đầu ống hướng vào tường thì vị trí ô đó chắc chắn sai . Công thức được giải thích như sau:

- số đầu ống nước hở: tổng số **đầu** ống nước không có kết nối, luôn là số chẵn:

![Imgur](https://i.imgur.com/iFuD2pl.png)

như hình trên thì tổng số đầu hở sẽ là 18 (hàng 1: 6, hàng 2: 3, hàng 3: 5, hàng 4: 4)

- Số ống không có nước: là tổng số ô không có nước, trong hình trên là 11

- Số đầu ống hướng vào tường: trong hình ví dụ có 8 đầu hướng vào tường

-  Số đầu ống deadend hướng vào nhau: ống deadend là ống chỉ có một head duy nhất và là ống cụt. Ở đây chỉ có một ống deadend hướng vào một ống deadend khác:

![Imgur](https://i.imgur.com/FLJh6yd.png)

- Số vòng lặp: ở đây không tồn tại vòng lặp nào được sinh bởi ống nên sẽ là 0

Như vậy hn có giá trị 18 / 2 + 11 + 8 * 5 + 1 * 5 + 0 * 3 = 65. Bài toán sẽ đạt goal state khi giá trị này đạt 0.

Dưới đây là mã giả cho giải thuật A* đã được trình bày:

```python

checking_states = [] 

hn = num_opened_head_ / 2 + num_no_water_ + num_wall_ * 5 + num_invalid_deadend_ * 5 + num_loop_ * 3     # gia tri hn khoi dau

chosen_state = (all_tiles, hn, [], 0)

visited = [chosen_state]

  

while not reach_goal(chosen_state):

	# loop qua từng ô để nó xoay qua bên phải (clockwise)
	for i, _ in enumerate(chosen_state[0]):

		right_lst = list_copy(chosen_state[0])

		num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = right_lst[i].rotate_clockwise(right_lst)

		# tính toán hn mới
		hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3

		gn = chosen_state[3] + 1 # tính toán gn mới từ gn cũ

		new_list_of_steps = chosen_state[2].append(right_lst[i].x, right_lst[i].y, 'right')
		new_state = (right_lst, hn, new_list_of_steps, gn)

		# cho vào list các state đang xem xét nếu nó chưa xuất hiện
		if not is_visited(new_state, visited):
			checking_states.append(new_state)


	# loop qua từng ô để nó xoay qua bên trái (anti clockwise)
	for i, _ in enumerate(chosen_state[0]):

		left_lst = list_copy(chosen_state[0])

		num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = left_lst[i].rotate_anti_clockwise(left_lst)

		# tính toán hn mới
		hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3

		gn = chosen_state[3] + 1 # tính toán gn mới từ gn cũ

		new_list_of_steps = chosen_state[2].append(left_lst[i].x, left_lst[i].y, 'left')
		new_state = (left_lst, hn, new_list_of_steps, gn)

		# cho vào list các state đang xem xét nếu nó chưa xuất hiện
		if not is_visited(new_state, visited):
			checking_states.append(new_state)
  
  
	# loop qua từng ô trong game để xoay nó hai lần	
	for i, _ in enumerate(chosen_state[0]):

		double_lst = list_copy(chosen_state[0])

		num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = double_lst[i].rotate_anti_clockwise(double_lst)
		num_opened_head, num_no_water, num_wall, num_invalid_deadend, num_loop = double_lst[i].rotate_anti_clockwise(double_lst)
		
		# tính toán hn mới
		hn = num_opened_head / 2 + num_no_water + num_wall * 5 + num_invalid_deadend * 5 + num_loop * 3

		gn = chosen_state[3] + 1 # tính toán gn mới từ gn cũ

		new_list_of_steps = chosen_state[2].append(double_lst[i].x, double_lst[i].y, 'left left')
		new_state = (double_lst, hn, new_list_of_steps, gn)

		# cho vào list các state đang xem xét nếu nó chưa xuất hiện
		if not is_visited(new_state, visited):
			checking_states.append(new_state)



	curr_min = 1_000_000

# Tìm trong checking state xem state nào có giá trị hn + gn bé nhất (tốt nhất) làm state được chọn cho lần lặp tiếp theo
	for state in checking_states:
		fn = state[1] + state[3]
		if fn <= curr_min:
			curr_min = fn
			chosen_state = state
	
	if len(checking_states) != 0:
		checking_states.remove(chosen_state)
	
	visited.append(chosen_state)
	
	if len(checking_states) == 0:
		break

```


# Phần thêm

Một bài giải 5x5 chờ hơi lâu mà có thể lấy vô làm ví dụ:))

![Imgur](https://i.imgur.com/Fo3htQq.png)

![Imgur](https://i.imgur.com/dsjlWKU.png)
# References


