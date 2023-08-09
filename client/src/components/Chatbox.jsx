import Slider from "react-slick"
import Flashcard from "./Flashcard"
import { FlashcardArray } from "react-quizlet-flashcard"
import InputBox from "./InputBox"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"
import "./customcss.css"
import AnswerBox from "./AnswerBox"

const SamplePrevArrow = (props) => {
  const { className, style, onClick } = props
  return (
    <div
      className={className}
      style={{ ...style, display: "block", color: "black" }} // Change color to black and adjust position
      onClick={onClick}
    >
      Previous
    </div>
  )
}

const SampleNextArrow = (props) => {
  const { className, style, onClick } = props
  return (
    <div
      className={className}
      style={{ ...style, display: "block", color: "black" }} // Change color to black and adjust position
      onClick={onClick}
    >
      Next
    </div>
  )
}

function Chatbox() {
  var settings = {
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    dots: false,
    prevArrow: <SamplePrevArrow />,
    nextArrow: <SampleNextArrow />,
  }

  const image_urls = [
    "https://mlsademo.blob.core.windows.net/imgdata/4a18ba8c-4eb1-4a5a-84eb-fa7a664cd88cWhatsApp%20Image%202023-08-02%20at%2022.01.472.jpg",
    "https://mlsademo.blob.core.windows.net/imgdata/7177094a-71f7-439e-8715-c86c0e940b20WhatsApp%20Image%202023-08-02%20at%2022.01.47.jpg",
  ]

  const questions = [
    {
      id: 1,
      backHTML: (
        <>
          Ronald Read was a former janitor who accumulated his wealth by saving
          what little he could and invested it in blue chip stocks. He waited
          for decades as tiny savings compounded into more than $8 million.
        </>
      ),
      frontHTML: <>Who was Ronald Read and how did he accumulate his wealth?</>,
    },
    {
      id: 2,
      backHTML: (
        <>
          Ronald Read was a former janitor who accumulated his wealth by saving
          what little he could and invested it in blue chip stocks. He waited
          for decades as tiny savings compounded into more than $8 million.
        </>
      ),
      frontHTML: <>Who was Ronald Read and how did he accumulate his wealth?</>,
    },
    {
      id: 3,
      backHTML: (
        <>
          Ronald Read was a former janitor who accumulated his wealth by saving
          what little he could and invested it in blue chip stocks. He waited
          for decades as tiny savings compounded into more than $8 million.
        </>
      ),
      frontHTML: <>Who was Ronald Read and how did he accumulate his wealth?</>,
    },
  ]

  const cards = [
    {
      question: "who is this",
      answer: "this is me",
    },
    {
      question: "who is this, subhashis",
      answer: "this is me, subhashis",
    },
  ]

  return (
    <>
      <div className="p-2">
        <h1 className="px-2 py-2 text-2xl font-bold border-b-2">
          Node.js Assignment
        </h1>
        <div className="px-2 py-4">
          <span className="text-md">Last Visited :</span>{" "}
          <span className="bg-fuchsia-300 text-fuchsia-800 px-2 py-1 font-medium rounded-md">
            12th August, 2023
          </span>
        </div>
        {/* <section></section> */}
        <div className="py-2 grid grid-cols-10 gap-8">
          <div className="col-span-4 col-start-1 flex items-center justify-center">
            <Slider {...settings} className="max-w-[25rem] mb-8">
              {image_urls.map((url, key) => {
                return (
                  <div key={key}>
                    {" "}
                    <img src={url} alt="" />
                  </div>
                )
              })}
            </Slider>
          </div>
          <div className="flex flex-col col-start-5 col-span-5">
            <div>
              <h1 className="text-2xl font-medium border-b-2 pb-2 mb-4">
                Flashcards
              </h1>
              <div className="flex">
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
                />
              </div>
            </div>
            <div className="mb-4">
              <h1 className="text-2xl font-medium border-b-2 pb-2 mb-2">
                Summary
              </h1>
              <p>
                The article discusses the lack of emphasis on soft skills in
                finance, leading to little improvement in the industry despite
                attracting top talent. It highlights the stories of a janitor
                who became wealthy through savings and investments, and a former
                Merrill Lynch executive who lost everything due to poor
                financial decisions. The author questions whether we have truly
                learned from trial and error in personal finance.
              </p>
            </div>
          </div>
        </div>
        <section className="py-2 px-4">
          <h1 className="text-2xl font-medium border-b-2 pb-2 mb-2">
            Chat QnA
          </h1>
          <div>
            <InputBox />
            <AnswerBox />
          </div>
        </section>
      </div>
    </>
  )
}

export default Chatbox
