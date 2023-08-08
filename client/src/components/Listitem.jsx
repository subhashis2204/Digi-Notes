import DescriptionIcon from "@mui/icons-material/Description"
import ErrorIcon from "@mui/icons-material/Error"

function ListItem({ title, isDue }) {
  return (
    <>
      <div className="flex items-center justify-between pr-2 hover:bg-slate-600 rounded-md">
        <div className="text-sm text-white px-2 py-3 flex items-center justify-start gap-2 ">
          <DescriptionIcon />
          {title}
        </div>
        {isDue ? <ErrorIcon className="text-white" /> : null}
      </div>
    </>
  )
}

export default ListItem
