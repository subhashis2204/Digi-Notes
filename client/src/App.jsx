import Sidebar from "./components/Sidebar"
import Chatbox from "./components/Chatbox"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"

function App() {
  return (
    <>
      <div className="grid grid-cols-6 md:grid-cols-10 absolute inset-0">
        <div className="col-start-1 col-span-3 md:col-span-2">
          <Sidebar />
        </div>
        <div className="col-start-3 col-span-3 md:col-span-8">
          <Chatbox />
        </div>
      </div>
    </>
  )
}

export default App
