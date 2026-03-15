# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.


## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  -> when i first opened the file it look good and organized but once i start playing and watch the rules thing started messing.The hint i get whikle playing where noot correct it just game me opposite guess to do when guessing 70 when the secret was 40 gave me "📈 Go HIGHER!" when I clearly needed to go lower. Likewise, i was able to pick numbers beyong the boundary 1-100. also the number changes with the even numbered attempt. initally i was chasing the moving target which i figure out later. 

---


## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

-> i used claude for this project to understand cetrain part of the code not the whole code. i was basically asking claude why there is frequant change in streamlit return and understand the probelm in deep. I frequasntly update and check the game ito see it it fixed or not. one time claude almost throw me up as it told me that hint bug wasw from flipped > and < comparisions whcih sound right but actually it was string causing that issue. some time even claude point me to the wrong line of code to fixed the game. 

---


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

-> i changed the code and use the developer debug info pannel to check if my code work as per my assumption or not. Running pytest on the starter tests also surfaced something real fast as check_guess retuen tuple like winr correct but that test asserted to be result ==win ie.e a plain string that why every test of mine failed initially. But i learned from it as it test me to see what actally the code need to turn to be true.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

-> I notice that the reason behind secret being changed is streamlit returns the whole python script from top to bottom on every new number it refrash every single time. later i fixed weapping the secret assigment inside the if "secret" not in st.session_state so that ir generate a new number which one deosnot already exist.
---


## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I want to make a habit of readng the error before asking AI to interpret it because i felt pytest failure message told me exactly wha was wrong before i evern asked. One thing I would do differently may be i write down my own theory behind why it happned. moreover i think different now how ai generated code can be buggy sometime more then human do and how it missed those details. 