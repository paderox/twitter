from tkinter import Tk, Label, Button, Radiobutton, IntVar

def ask_multiple_choice_question(prompt, options):
    root = Tk()
    if prompt:
        Label(root, text=prompt).pack()
    v = IntVar()
    for i, option in enumerate(options):
        Radiobutton(root, text=option, variable=v, value=i).pack(anchor="w")
    Button(text="Submit", command=root.destroy).pack()
    root.mainloop()
    if v.get() == 0: return None
    return options[v.get()]

result = ask_multiple_choice_question(
    "What is your favorite color?",
    [
        "Blue!",
        "No -- Yellow!",
        "Aaaaargh!"
    ]
)

print("User's response was: {}".format(repr(result)))