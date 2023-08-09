import { useState } from "react"

function AnswerBox() {
  const [answer, setAnswer] = useState("")

  const initializeSession = (
    <div className="text-center pt-2">
      <button className="bg-green-700 px-3 py-2 rounded-md text-white">
        Initialize Session
      </button>
    </div>
  )

  const answerBox = <div className="p-2 bg-gray-300 mt-2">{answer}</div>

  const content = answer === "" ? initializeSession : answerBox

  return (
    <>
      <div>{content}</div>
    </>
  )
}

export default AnswerBox
