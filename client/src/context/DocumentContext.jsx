import { createContext } from "react"

const DocumentContext = createContext()

function Provider({ children }) {
  return <DocumentContext.Provider>{children}</DocumentContext.Provider>
}

export default DocumentContext
export { Provider }
