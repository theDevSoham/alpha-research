import { useEffect, useState } from "react";
import { getPeople, enrichPerson } from "../services/api";
import Loader from "./Loader";

export interface IPeople {
  id: string;
  full_name: string;
  email: string;
  title: string;
  company: {
    id: string;
    name: string;
  };
  created_at: string;
}

const PeopleList: React.FC<{
  onEnrichTrigger?: (jobId: string, people: IPeople) => void;
}> = ({ onEnrichTrigger }) => {
  const [people, setPeople] = useState<IPeople[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getPeople()
      .then((res) => {
        console.log("Get people: ", res.request, res.data);
        setPeople(res.data);
        setLoading(false);
      })
      .catch((e) => {
        console.error("Error fetching people: ", e);
        setLoading(false);
      });
  }, []);

  const handleEnrich = async (person: IPeople) => {
    try {
      const res = await enrichPerson(person.id);
      if (res.status !== 200) {
        alert("Failed to enrich");
        return;
      }
      alert("Research agent triggered!");
      if (onEnrichTrigger) onEnrichTrigger(res.data?.task_id, person);
    } catch (error) {
      alert("Error: Data cannot be enriched at the moment");
      console.error(error);
    }
  };

  return (
    <div className="w-full h-98 flex flex-col justify-center items-center">
      <h1 className="text-xl font-bold mb-4">People</h1>
      {loading ? (
        <div className="w-full h-20 flex justify-center items-center">
          <Loader />
        </div>
      ) : (
        <ul className="w-full flex flex-col gap-3">
          {people.map((p) => (
            <li
              key={p.id}
              className="w-full bg-white shadow-md rounded p-4 flex justify-between items-center"
              style={{ padding: "1rem 2rem" }}
            >
              <div>
                <div className="font-semibold">{p.full_name}</div>
                <div className="text-sm text-gray-600">
                  {p.title} @ {p.company.name}
                </div>
                <div className="text-xs text-gray-400">{p.email}</div>
              </div>
              <button
                onClick={() => handleEnrich(p)}
                className="bg-blue-500 text-white rounded cursor-pointer"
                style={{ padding: "4px 8px" }}
              >
                Run Research
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PeopleList;
