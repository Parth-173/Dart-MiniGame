import random
import subprocess
import tkinter as tk
from PIL import Image, ImageTk

class Dartboard:
    def __init__(self):
        self.sections = ["Easy", "Medium", "Hard"]

    def throw_dart(self):
        return random.choice(self.sections)

class CodingContest:
    def __init__(self):
        self.questions = {
            "Easy": ["Write a Python function to calculate the factorial of a number.",
                     "Write a program to find the largest element in an array.",
                    ],
            "Medium": ["Write a program to sort elements in an array using the bubble sort algorithm.",
                       "Implement a function to convert a decimal number to binary.",
                      ],
            "Hard": ["Implement a function to find all permutations of a given string.",
                     "Write a program to implement the merge sort algorithm.",
                    ]
        }
        self.current_question = None
        self.current_difficulty = None
        self.question_index = 0
    
    def get_question(self, difficulty):
        if self.question_index >= len(self.questions[difficulty]):
            return None
        self.current_question = self.questions[difficulty][self.question_index]
        self.question_index += 1
        return self.current_question

    def solve_question(self, code_text, output_text):
        code = code_text.get("1.0", tk.END)
        output = self.execute_code(code)
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, "Your code output:\n")
        output_text.insert(tk.END, output)
        output_text.config(state=tk.DISABLED)

    def execute_code(self, code):
        with open("participant_code.py", "w") as f:
            f.write(code)
        output = subprocess.run(["python", "participant_code.py"], capture_output=True, text=True)

        return output.stdout

    def next_question(self, window, code_text, output_text):
        self.question_index = 0
        self.current_difficulty = None
        self.current_question = None
        self.display_next_question(window, code_text, output_text)

    def display_next_question(self, window, code_text, output_text):
        if self.current_difficulty is None or self.question_index >= len(self.questions[self.current_difficulty]):
            self.current_difficulty = dartboard.throw_dart()
        question = self.get_question(self.current_difficulty)
        if question:
            question_label.config(text=f"Question : {question}")
        else:
            question_label.config(text="No more questions")
            next_button.config(state=tk.DISABLED)
        code_text.delete("1.0", tk.END)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    dartboard = Dartboard()
    contest = CodingContest()

    window = tk.Tk()
    window.title("Coding Contest")

    background_image = Image.open("wp9358220.webp")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(window, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    question_label = tk.Label(window, text="Question: ", wraplength=700, fg="green", bg="black", font=("Helvetica", 16))
    question_label.pack(padx=10, pady=10)

    code_text = tk.Text(window, wrap=tk.WORD, height=10, width=60, fg="green", bg="black", font=("Courier", 14))
    code_text.pack(padx=10, pady=10)

    output_text = tk.Text(window, wrap=tk.WORD, height=10, width=60, fg="green", bg="black", font=("Courier", 14))
    output_text.pack(padx=10, pady=10)
    output_text.config(state=tk.DISABLED)

    submit_button = tk.Button(window, text="Submit", command=lambda: contest.solve_question(code_text, output_text), fg="red", bg="black", font=("Helvetica", 12))
    submit_button.pack(pady=5)

    next_button = tk.Button(window, text="Next", command=lambda: contest.next_question(window, code_text, output_text), fg="red", bg="black", font=("Helvetica", 12))
    next_button.pack(pady=5)

    contest.display_next_question(window, code_text, output_text)

    window.mainloop()
