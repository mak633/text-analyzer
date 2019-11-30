const puppeteer = require('puppeteer');
const writer = require('./write_txt');

(async () => {
  const links = await getLinks();
  const texts = await getTexts(links);

  texts.forEach((t, i) => {
    console.log(`Writing to file text ${i + 1} of ${texts.length}`);
    writer.writeFn(t.split('.'));
  });
})();

async function getLinks() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  let result = [];

  const baseUrl = 'https://www.eurointegration.com.ua/articles/';
  const linksSelector = '.block_stories .article .article__title a';
  const lastPage = 46;
  const urls = [baseUrl];

  for (let i = 1; i <= lastPage; i++) {
    urls.push(`${baseUrl}page_${i}/`);
  }

  let links = [];
  for (let i = 0; i < urls.length; i++) {
    console.log(`Get links from ${urls[i]}`);
    await page.goto(urls[i]);
    links = await page.$$eval(linksSelector, links => links.map(l => l.href));
    result = result.concat(links);
  }

  await browser.close();

  return result;
}

async function getTexts(links) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const result = [];
  let text;

  for (let i = 0; i < links.length; i++) {
    text = null;

    try {
      console.log(`Grab text ${i} of ${links.length} from ${links[i]}`);
      text = await getTextByLink(links[i]);
    } catch(e) {
      console.error(`ERROR: Couldn't get text from ${links[i]}\n${e}\n`,);
    }

    if (text) result.push(text);
  }

  await browser.close();
  return result;

  async function getTextByLink(link) {
    await page.goto(link);
    html = await page.$eval('.post__text', text => text.innerHTML);
    return formatText(html);
  }

  function formatText(text) {
    return text.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').replace(/\d/g,'').replace('&nbsp;', ' ');
  }
}
