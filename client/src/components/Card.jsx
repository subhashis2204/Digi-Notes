import { useState } from "react"

function Card({ question, answer }) {
  const [isFlipped, setIsFlipped] = useState(false)

  const handleClick = () => {
    setIsFlipped(!isFlipped)
  }

  const content = isFlipped ? answer : question

  return (
    <>
      <div
        className="w-[15rem] h-[10rem] rounded-md bg-yellow-100"
        onClick={handleClick}
      >
        <div>{content}</div>
      </div>
    </>
  )
}

export default Card
