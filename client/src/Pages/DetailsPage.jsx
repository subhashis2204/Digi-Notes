import axios from "axios"
import { useState, useEffect } from "react"
import Carousel from "../components/Carousel"
import PageHeader from "../components/PageHeader"
import Flashcards from "../components/Flashcards"

function DetailsPage({ document }) {
  const [documentData, setDocumentData] = useState({})

  const { title, image_urls, last_updated, flashcards } = documentData

  console.log(document, "this is from the details page")

  useEffect(() => {
    const fetchDocument = async () => {
      const response = await axios.get(
        `http://localhost:8000/uploads/${document}`
      )

      console.log(response.data.answer)
      setDocumentData(response.data.answer)
    }

    fetchDocument()
  }, [document])

  console.log(flashcards)

  return (
    <>
      <div>
        <PageHeader title={title} lastVisited={last_updated} />
        <section className="grid grid-cols-12 gap-4">
          <section className="col-start-1 col-span-6 flex justify-center">
            <Carousel image_urls={image_urls} />
          </section>
          <section className="col-start-7 col-span-6">
            <Flashcards flashcards={flashcards} />
          </section>
        </section>
      </div>
    </>
  )
}

export default DetailsPage
