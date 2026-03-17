self.onmessage = (e: MessageEvent<string[]>) => {
  const words = e.data;
  const byCompactness = findBestCrosswords(words);
  self.postMessage(byCompactness);
};


type wordPosition = {
  x: number,
  y: number,
  across: boolean,
}

function key(x: number, y: number): number {
  return x + y * 1000;
}

function permutations<T>(arr: T[]): T[][] {
  let out: T[][] = [];

  const _permute = (l: T[], m: T[] = []) => {
    if (l.length === 0) {
      out.push(m)
    } else {
      for (let i = 0; i < l.length; i++) {
        let curr = l.slice();
        let next = curr.splice(i, 1);
        _permute(curr.slice(), m.concat(next))
      }
    }
  }

  _permute(arr)

  return out;
}

function shuffleArray<T>(array: T[]) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * array.length);
    [array[i], array[j]] = [array[j], array[i]];
  }
}

type CrosswordGrid = Map<number, string>;

type CrosswordSpec = {
  grid: CrosswordGrid,
  positions: Map<string, wordPosition>,
}

function withWord(spec: CrosswordSpec, newWord: string): CrosswordSpec[] {
  const out: CrosswordSpec[] = [];

  spec.positions.forEach((position, word) => {
    for (let i = 0; i < word.length; i++) {
      for (let j = 0; j < newWord.length; j++) {
        if (newWord[j] === word[i]) {
          const newSpec: CrosswordSpec = {
            grid: new Map(spec.grid),
            positions: new Map(spec.positions),
          };

          let fits: boolean = true;
          if (position.across) {
            const newPosition: wordPosition = {
              x: position.x + i,
              y: position.y - j,
              across: false,
            };

            if (
              newSpec.grid.has(key(newPosition.x, newPosition.y - 1))
              || newSpec.grid.has(key(newPosition.x, newPosition.y + newWord.length))
            ) {
              fits = false;
            }

            if (fits) {
              for (let dy = 0; dy < newWord.length; dy++) {
                const k = key(newPosition.x, newPosition.y + dy);
                if (
                  (newSpec.grid.has(k) && newSpec.grid.get(k) != newWord[dy])
                  || (!newSpec.grid.has(k) && (
                    newSpec.grid.has(key(newPosition.x - 1, newPosition.y + dy))
                    || newSpec.grid.has(key(newPosition.x + 1, newPosition.y + dy))
                  ))
                ) {
                  fits = false;
                  break;
                } else {
                  newSpec.positions.set(newWord, newPosition);
                  newSpec.grid.set(k, newWord[dy]);
                }
              }
            }
          } else {
            const newPosition: wordPosition = {
              x: position.x - j,
              y: position.y + i,
              across: true,
            };

            if (
              newSpec.grid.has(key(newPosition.x - 1, newPosition.y))
              || newSpec.grid.has(key(newPosition.x + newWord.length, newPosition.y))
            ) {
              fits = false;
            }

            if (fits) {
              for (let dx = 0; dx < newWord.length; dx++) {
                const k = key(newPosition.x + dx, newPosition.y);
                if (
                  (newSpec.grid.has(k) && newSpec.grid.get(k) != newWord[dx])
                  || (!newSpec.grid.has(k) && (
                    newSpec.grid.has(key(newPosition.x + dx, newPosition.y - 1))
                    || newSpec.grid.has(key(newPosition.x + dx, newPosition.y + 1))
                  ))
                ) {
                  fits = false;
                  break;
                } else {
                  newSpec.positions.set(newWord, newPosition);
                  newSpec.grid.set(k, newWord[dx]);
                }
              }
            }
          }

          if (fits) {
            out.push(newSpec);
          }
        }
      }
    }
  })

  return out;
}

function startingSpec(word: string, across: boolean): CrosswordSpec {
  const positions = new Map<string, wordPosition>([
    [
      word,
      {
        x: 0,
        y: 0,
        across,
      },
    ],
  ]);

  const grid = new Map<number, string>();

  for (let i = 0; i < word.length; i++) {
    if (across) {
      grid.set(key(i, 0), word[i]);
    } else {
      grid.set(key(0, i), word[i]);
    }
  }

  return {grid, positions};
}

function addWordsInOrder(words: string[]): CrosswordSpec[] {
  let specs: CrosswordSpec[] = [
    startingSpec(words[0], true),
    startingSpec(words[0], false),
  ];

  words.slice(1).forEach(word => {
    const newSpecs: CrosswordSpec[] = [];

    specs.forEach(spec => {
      newSpecs.push(...withWord(spec, word));
    })

    specs = newSpecs;
  });

  return specs;
}

function toString(spec: CrosswordSpec): string {
  let startX = 0, startY = 0, endX = 0, endY = 0;

  spec.positions.forEach((position, word) => {
    startX = Math.min(startX, position.x);
    startY = Math.min(startY, position.y);

    if (position.across) {
      endX = Math.max(endX, position.x + word.length);
      endY = Math.max(endY, position.y + 1);
    } else {
      endX = Math.max(endX, position.x + 1);
      endY = Math.max(endY, position.y + word.length);
    }
  });

  let out = "";

  for (let y = startY; y < endY; y++) {
    if (y > startY) {
      out += "\n"
    }

    for (let x = startX; x < endX; x++) {
      if (x > startX) {
        out += "|"
      }

      out += spec.grid.get(key(x, y)) || " ";
    }
  }

  return out;
}

const optionsSize = 10;
const allPermsMaxElements = 9;
const numPerms = 100;
const timeLimit = 5000;

function getPerms(words: string[]): string[][] {
  if (words.length <= allPermsMaxElements) {
    const perms = permutations(words);

    console.log("perms done");

    shuffleArray(perms);

    console.log("shuffle done");

    return perms;
  } else {
    const copyWords = words.slice();
    const perms = [];
    for (let i = 0; i < numPerms; i++) {
      shuffleArray(copyWords);
      perms.push(copyWords.slice());
    }
    console.log("perms done");
    return perms;
  }
}

function findBestCrosswords(words: string[]): [number, string, CrosswordSpec][] {
  let byCompactness: [number, string, CrosswordSpec][] = [];
  const startTime = new Date().getTime();

  const perms = getPerms(words);

  for (let i = 0; i < perms.length; i++) {
    if ((new Date()).getTime() - startTime > timeLimit) {
      console.log(`${i} rounds completed.`)
      break;
    }

    const wordlist = perms[i];
    const newSpecs = addWordsInOrder(wordlist);
    console.log(`Round ${i + 1} found ${newSpecs.length} specs`);
    const alreadyFound = new Set(byCompactness.map(([_, st, __]) => st));

    let minLen = 10000;
    if (byCompactness.length > 0) {
      const [_, st, __] = byCompactness[byCompactness.length - 1];
      minLen = st.length;
    }

    newSpecs.forEach(spec => {
      const crosswordString = toString(spec);
      if (crosswordString.length <= minLen && !alreadyFound.has(crosswordString)) {
        byCompactness.push([crosswordString.length, crosswordString, spec]);
        alreadyFound.add(crosswordString);
      }
    });

    alreadyFound.clear();

    console.log(`sorting ${byCompactness.length} items`);
    byCompactness.sort((a, b) => a[0] - b[0]);
    byCompactness = byCompactness.slice(0, optionsSize);
    console.log(`After round ${i + 1}`);
  }

  console.log(byCompactness);

  return byCompactness;
}

export {}
