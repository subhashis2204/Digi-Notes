import ListItem from "./Listitem"

function Sidebar() {
  const content = [
    {
      id: 1,
      title: "Node.js Assignment",
      isDue: true,
    },
    {
      id: 2,
      title: "Biology Homework",
      isDue: false,
    },
    {
      id: 3,
      title: "HR Assignment",
      isDue: true,
    },
  ]

  const renderedItems = content.map((item) => {
    return <ListItem key={item.id} title={item.title} isDue={item.isDue} />
  })

  return (
    <>
      <div className="relative p-2 pt-3 flex flex-col gap-2 bg-sidebar-gray h-full">
        <div className="text-md font-medium text-center">
          <button className="p-2 border-2 border-gray-500 rounded-lg w-full text-white">
            New Session
          </button>
        </div>
        <div className="flex flex-col gap-1">{renderedItems}</div>
      </div>
    </>
  )
}

export default Sidebar
