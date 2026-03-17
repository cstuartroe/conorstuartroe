import React, {useState, useRef, useEffect} from "react";

// const words = ["albatross", "saturday", "quince", "mustard", "science", "kitten", "buttock", "pope", "peanut", "gross", "halibut"];
// const words = ["coco", "niko", "winnie", "rue", "japan", "ktown", "trapp", "qcspa"];


type Props = {};

export default function Crossword(_props: Props) {
  const [userInput, setUserInput] = useState<string>("");
  const [crosswords, setCrosswords] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const workerRef = useRef<Worker | null>(null);
  // Clean up the worker if the component unmounts
  useEffect(() => {
    return () => {
      if (workerRef.current) {
        workerRef.current.terminate();
      }
    };
  }, []);

  return (
    <div style={{padding: "5vh"}}>
      <p style={{textAlign: "center"}}>Input your words below, separated by commas:</p>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        style={{width: '100%'}}
      />
      <button
        style={{margin: "auto", display: "flex"}}
        onClick={() => {
          setLoading(true);
          setErrorMessage("");
          const words = userInput.split(",").map(word => word.trim().toLocaleUpperCase());

          // Terminate existing worker if the user clicks "Generate!" multiple times
          if (workerRef.current) {
            workerRef.current.terminate();
          }

          // Initialize the worker. The path must point to the worker file created in step 1.
          workerRef.current = new Worker(new URL('./crossword.worker.ts', import.meta.url), {
            type: 'module'
          });

          // Listen for the result from the worker
          workerRef.current.onmessage = (e: MessageEvent<[number, string, any][]>) => {
            const res = e.data;
            console.log(res);
            setCrosswords(res.map(([_, crossword, __]) => crossword));
            setLoading(false);
            if (res.length === 0) {
              setErrorMessage("Not possible for that set of words.")
            }

            // Cleanup worker after completion
            workerRef.current?.terminate();
            workerRef.current = null;
          };

          // Send the data to the background thread
          workerRef.current.postMessage(words);
        }}
      >
        Generate!
      </button>
      {errorMessage && (
        <p style={{textAlign: "center", color: "red"}}>{errorMessage}</p>
      )}
      {loading ? (
        <p>Loading...</p>
      ) : (
        crosswords.map((crossword, i) => (
          <div style={{marginTop: "2vh", width: "100%"}} key={crossword}>
            <table style={{margin: "0px auto"}}>
              <tbody>
              {crossword.split("\n").map((line, j) => (
                <tr key={j}>
                  {line.split("|").map((c, i) => (
                    <td
                      key={i}
                      style={{
                        border: "1px solid black",
                        textAlign: "center",
                        backgroundColor: c === " " ? "black" : "white",
                        height: "2vh",
                        width: "2vh",
                        fontSize: "1.5vh",
                        fontFamily: "Times New Roman",
                      }}
                    >
                      {c}
                    </td>
                  ))}
                </tr>
              ))}
              </tbody>
            </table>
          </div>
        ))
      )}
    </div>
  );
}
