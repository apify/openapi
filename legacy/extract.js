links = []; document.querySelectorAll("a").forEach((e)=>{if(e.href.indexOf("https://docs.apify.com/api/v2#") > -1) { links.push({link: e.href, text:e.innerText.replace(/(\r\n|\n|\r)/gm, "").trim()})}})

dedupLinks = links.filter((value, index, self) =>
  index === self.findIndex((t) => (
    t.link === value.link && t.text === value.text
  ))
)

dedupLinks
