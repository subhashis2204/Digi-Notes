import Sidebar from "./components/Sidebar"
import Chatbox from "./components/Chatbox"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"
import { useEffect, useState } from "react"

import DetailsPage from "./Pages/DetailsPage"
import UploadPage from "./Pages/UploadPage"
import axios from "axios"

function App() {
  const [allDocuments, setAllDocuments] = useState([])
  const [document, setDocument] = useState(null)

  useEffect(() => {
    const fetchDocuments = async () => {
      const response = await axios.get("http://localhost:8000/")

      setAllDocuments(response.data.message)

      console.log(response.data.message)
    }

    fetchDocuments()
  }, [])

  const content =
    document === null ? <UploadPage /> : <DetailsPage document={document} />

  return (
    <>
      <div className="grid grid-cols-6 md:grid-cols-10 absolute inset-0">
        <div className="col-start-1 col-span-3 md:col-span-2">
          <Sidebar content={allDocuments} setDocument={setDocument} />
        </div>
        <div className="col-start-3 col-span-3 md:col-span-8">
          {/* {document} */}
          {/* <Chatbox /> */}
          {content}
        </div>
      </div>
    </>
  )
}

export default App
