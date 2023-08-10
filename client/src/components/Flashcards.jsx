import { FlashcardArray } from "react-quizlet-flashcard"
import Heading from "./Heading"

function Flashcards({ flashcards }) {
  if (!flashcards) return <></>

  const questions = flashcards.map((flashcard, index) => {
    return {
      id: index,
      frontHTML: flashcard.question,
      backHTML: flashcard.answer,
    }
  })

  console.log(questions)
  return (
    <>
      <Heading>Flashcards</Heading>
      <FlashcardArray
        cards={questions}
        frontContentStyle={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: "1.2rem",
          padding: "2rem",
          textAlign: "center",
          backgroundColor: "lightgoldenrodyellow",
          color: "black",
        }}
        backContentStyle={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: "1.2rem",
          padding: "2rem",
          textAlign: "center",
          backgroundColor: "lightgoldenrodyellow",
          color: "black",
        }}
        cycle
      />
    </>
  )
}

export default Flashcards
