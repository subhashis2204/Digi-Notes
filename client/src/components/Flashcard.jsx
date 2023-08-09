import { useState } from "react"
import Card from "./Card"

function Flashcard({ cards }) {
  const [currentCard, setCurrentCard] = useState(0)

  const handleNext = () => {
    setCurrentCard((currentCard + 1) % cards.length)
  }
  const handlePrev = () => {
    setCurrentCard((currentCard - 1) % cards.length)
  }

  return (
    <>
      <div>
        <div></div>
        <button onClick={handlePrev}> prev </button>
        <button onClick={handleNext}> next </button>
      </div>
    </>
  )
}

export default Flashcard
