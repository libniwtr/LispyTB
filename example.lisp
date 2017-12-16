(let ((myZ (+ "this is note " Name Text))
      (myX (* 1 2 3 (+ 3 4 5)))
      (myY (. "XX;YY;ZZ" (at 2))))
  (set! MyDate (max (list MyDateA, MyDateB)))
  (set! MyDate (. links outbound attended ($ MyDate)))
  (if (not (. Text (contains "like")))
      (begin
       (set! Color "red")
       (set! Width 3.5))
    (set! Color "blue"))
  (cond ((eq Color "red")
         (set! Color2 "blue"))
        ((eq Color "blue")
         (set! Color2 "red"))
        (else
         (begin
          (set! Color2 "green")
          (set! Text "You are lucky!")))))


