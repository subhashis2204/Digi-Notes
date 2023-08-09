function InputBox() {
  return (
    <>
      <form action="" className="p-2 border-2 flex rounded-md">
        <input
          type="text"
          className="bg-slate-100 p-2 rounded-md grow mr-2 outline-0 border-2 border-gray-300"
          placeholder="Please Type Your Question Here"
        />
        <button
          type="submit"
          className="bg-green-700 px-3 py-2 rounded-md text-white"
        >
          Send
        </button>
      </form>
    </>
  )
}

export default InputBox
