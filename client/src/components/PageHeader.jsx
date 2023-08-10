function PageHeader({ title, lastVisited }) {
  return (
    <>
      <h1 className="px-2 py-2 text-2xl font-bold border-b-2">{title}</h1>
      <div className="px-2 py-4">
        <span className="text-md">Last Visited :</span>{" "}
        <span className="bg-fuchsia-300 text-fuchsia-800 px-2 py-1 font-medium rounded-md">
          {lastVisited}
        </span>
      </div>
    </>
  )
}

export default PageHeader
