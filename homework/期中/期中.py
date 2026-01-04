import random

def play_game():
    # 1. 設定遊戲參數
    min_num = 1
    max_num = 1000
    max_attempts = 5
    
    # 2. 產生謎底
    answer = random.randint(min_num, max_num)
    attempts_used = 0  # 目前用掉幾次
    
    print(f"=== 終極猜數字 ({min_num}-{max_num}) ===")
    print(f"挑戰：請在 {max_attempts} 次內猜中（數學上極難！）\n")

    # 3. 使用 while 迴圈，直到次數用完或猜中
    while attempts_used < max_attempts:
        try:
            # 顯示剩餘次數
            print(f"剩餘機會: {max_attempts - attempts_used}")
            user_input = input("請輸入數字: ")
            
            # 轉換輸入
            guess = int(user_input)
            
            # 檢查範圍 (如果超出範圍，直接進入下一輪迴圈，不扣次數)
            if guess < min_num or guess > max_num:
                print(f"⚠️ 警告：請輸入 {min_num} 到 {max_num} 之間的數字！(不扣次數)\n")
                continue
            
            # --- 只要程式跑到這裡，代表輸入是有效的，次數 +1 ---
            attempts_used += 1

            # 核心判斷
            if guess == answer:
                print(f"\n🎉 恭喜！你在第 {attempts_used} 次猜對了！答案是 {answer}。")
                return # 結束函式
            elif guess < answer:
                print("❌ 太小了 (Higher)\n")
            else:
                print("❌ 太大了 (Lower)\n")
                
        except ValueError:
            print("⚠️ 格式錯誤：請輸入整數！(不扣次數)\n")

    # 4. 迴圈結束代表輸了
    print(f"💀 遊戲結束！正確答案是：{answer}")

if __name__ == "__main__":
    play_game()