import React, { useState, useEffect } from "react"
import Slider from "react-slick"

function Carousel({ image_urls }) {
  const [imagesLoaded, setImagesLoaded] = useState(false)

  useEffect(() => {
    const preloadImages = async () => {
      try {
        const promises = image_urls.map((url) => {
          return new Promise((resolve, reject) => {
            const img = new Image()
            img.onload = resolve
            img.onerror = reject
            img.src = url
          })
        })

        await Promise.all(promises)
        setImagesLoaded(true)
      } catch (error) {
        console.error("Error preloading images:", error)
      }
    }

    preloadImages()
  }, [image_urls])

  if (!imagesLoaded) {
    return <div>Loading...</div>
  }

  const settings = {
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: true,
    dots: false,
  }

  return (
    <>
      <Slider {...settings} className="max-w-[25rem]">
        {image_urls &&
          image_urls.map((url, key) => (
            <div key={key}>
              <img src={url} alt="" />
            </div>
          ))}
      </Slider>
    </>
  )
}

export default Carousel
