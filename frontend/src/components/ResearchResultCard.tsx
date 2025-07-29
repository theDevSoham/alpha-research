export interface Person {
  full_name: string;
  profile_url: string;
  title: string;
  current_company: string;
  location: string;
  summary: string;
  social_presence?: Record<string, string>;
}

export interface SearchRanking {
  top_result_position: number;
  source: string;
  search_query: string;
  search_url: string;
}

export interface PublicWebPresence {
  official_website_found: boolean;
  search_rankings: Record<string, SearchRanking>;
}

export interface Company {
  name: string;
  role_of_person: string;
  mentioned_by: string;
  public_web_presence: PublicWebPresence;
  product_description_available: boolean;
  description: string;
  requires_further_research: boolean;
}

export interface Meta {
  data_source: string;
  query: string;
  timestamp_utc: string;
  total_results: number;
  api_url: string;
}

export interface ResearchResult {
  id: string;
  entity_type: string;
  entity_id: string;
  snippet_type: string;
  payload: {
    person: Person;
    company: Company;
    meta: Meta;
  };
  source_urls: string[];
  created_at: string;
}

interface Props {
  result: ResearchResult;
}

export default function ResearchCard({ result }: Props) {
  const { person, company, meta } = result.payload;

  return (
    <div
      className="bg-white shadow-lg rounded-lg w-full max-w-2xl mx-auto flex flex-col gap-6"
      style={{ padding: "30px", marginBottom: "30px" }}
    >
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        📊 Research Summary
      </h2>

      {/* Person Info */}
      <div className="mb-2">
        <strong className="text-gray-700">🙍 Person:</strong>
        <p className="text-gray-600">
          <a
            href={person.profile_url}
            className="text-blue-600"
            target="_blank"
            rel="noreferrer"
          >
            {person.full_name}
          </a>{" "}
          – {person.title} @ {person.current_company}
        </p>
        <p className="text-gray-600 italic">{person.location}</p>
        <p className="text-gray-600">{person.summary}</p>
      </div>

      {/* Social Presence */}
      {person.social_presence && (
        <div className="mb-2">
          <strong className="text-gray-700">🌐 Social Presence:</strong>
          <ul className="list-disc ml-5 text-blue-600">
            {Object.entries(person.social_presence).map(([platform, url]) => (
              <li key={platform}>
                <a href={url} target="_blank" rel="noreferrer">
                  {platform}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Company Info */}
      <div className="mb-2">
        <strong className="text-gray-700">🏢 Company:</strong>
        <p className="text-gray-600">
          {company.name} – Role: {company.role_of_person}
        </p>
        <p className="text-gray-600">Mentioned by: {company.mentioned_by}</p>
        <p className="text-gray-600">Description: {company.description}</p>
        {company.requires_further_research && (
          <p className="text-red-600 font-semibold">
            ⚠️ Requires Further Research
          </p>
        )}
      </div>

      {/* Public Web Presence */}
      <div className="mb-2">
        <strong className="text-gray-700">🌍 Web Presence:</strong>
        <p className="text-gray-600">
          Official Website Found:{" "}
          {company.public_web_presence.official_website_found
            ? "✅ Yes"
            : "❌ No"}
        </p>
        <div className="ml-4">
          {Object.entries(company.public_web_presence.search_rankings).map(
            ([engine, rank]) => (
              <div key={engine}>
                <strong>{engine}</strong>:{" "}
                <a
                  href={rank.search_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-600"
                >
                  {rank.search_query}
                </a>{" "}
                – Rank #{rank.top_result_position}
              </div>
            )
          )}
        </div>
      </div>

      {/* Metadata */}
      <div className="mb-2">
        <strong className="text-gray-700">🧾 Meta:</strong>
        <p className="text-gray-600">
          Source: {meta.data_source} | Queried: {meta.query}
        </p>
        <p className="text-gray-600">Timestamp: {meta.timestamp_utc}</p>
        <p className="text-blue-600">
          <a href={meta.api_url} target="_blank" rel="noreferrer">
            API Link 🔗
          </a>
        </p>
      </div>

      {/* Source URLs */}
      <div className="mb-2">
        <strong className="text-gray-700">🔗 Sources:</strong>
        <ul className="list-disc ml-5 text-blue-600">
          {result.source_urls.map((url, i) => (
            <li key={i}>
              <a href={url} target="_blank" rel="noopener noreferrer">
                {url}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
