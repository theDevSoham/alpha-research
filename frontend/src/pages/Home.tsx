import { useState } from "react";
import PeopleList, { type IPeople } from "../components/PeopleList";
import ProgressBar from "../components/Progressbar";
import ResearchCard, {
  type ResearchResult,
} from "../components/ResearchResultCard";
import { getSnippets } from "../services/api";

const Home = () => {
  const [showProgress, setShowProgress] = useState<boolean>(false);
  const [jobId, setJobId] = useState<string>("");
  const [selectedPerson, setSelectedPerson] = useState<IPeople | null>(null);
  const [enrichResult, setEnrichResult] = useState<ResearchResult | null>(null);

  const populateResearchResult = async () => {
    try {
      const { data } = await getSnippets(selectedPerson?.company.id as string);

      if (!Array.isArray(data)) {
        alert("Failed to fetch data");
        return;
      }

      console.log("Enrich: ", data);
      setEnrichResult({
        ...data?.[0]?.payload,
        source_urls: data?.[0]?.source_urls,
      });
    } catch (error) {
      console.error(error);
      alert("Error: Feching enrich data failed");
    }
  };

  return (
    <div
      className="max-w-2xl mt-10 lg:py-20 py-10 flex flex-col gap-10"
      style={{ margin: "auto" }}
    >
      {showProgress && jobId && (
        <ProgressBar
          jobId={jobId}
          onComplete={() => {
            console.log("Completed");
            setShowProgress(false);
            setJobId("");
            populateResearchResult();
          }}
        />
      )}
      <PeopleList
        onEnrichTrigger={(taskId, person) => {
          setJobId(taskId);
          setShowProgress(true);
          setSelectedPerson(person);
        }}
      />

      {enrichResult && <ResearchCard result={enrichResult} />}
    </div>
  );
};

export default Home;
