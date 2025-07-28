import { useState } from "react";
import PeopleList, { type IPeople } from "../components/PeopleList";
import ProgressBar from "../components/Progressbar";
import ResearchCard, {
  type ResearchResult,
} from "../components/ResearchResultCard";
import {
  reseedPeople,
  unseedPeople,
  unenrichPeople,
} from "../services/dev_tools";
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

  const handleSeed = async () => {
    try {
      await reseedPeople();
      alert("Seeded successfully");
    } catch (e) {
      alert("Failed to seed");
    }
  };

  const handleUnseed = async () => {
    try {
      await unseedPeople();
      alert("Unseeded successfully");
    } catch (e) {
      alert("Failed to unseed");
    }
  };

  const handleUnenrich = async () => {
    try {
      await unenrichPeople();
      alert("Unenriched successfully");
    } catch (e) {
      alert("Failed to unenrich");
    }
  };

  return (
    <div
      className="max-w-2xl mt-10 lg:py-20 py-10 flex flex-col gap-10"
      style={{ margin: "auto" }}
    >
      {/* Dev-only buttons */}
      <div className="flex gap-4 justify-center" style={{ padding: "20px 0" }}>
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          onClick={handleSeed}
          style={{ padding: "4px 8px" }}
        >
          Seed
        </button>
        <button
          className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
          onClick={handleUnseed}
          style={{ padding: "4px 8px" }}
        >
          Unseed
        </button>
        <button
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          onClick={handleUnenrich}
          style={{ padding: "4px 8px" }}
        >
          Unenrich
        </button>
      </div>

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
