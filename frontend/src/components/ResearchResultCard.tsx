export interface ResearchResult {
  company_value_prop: string;
  product_names: string[];
  pricing_model: string;
  key_competitors: string[];
  company_domain: string;
  source_urls: string[];
}

interface Props {
  result: ResearchResult;
}

export default function ResearchCard({ result }: Props) {
  return (
    <div
      className="bg-white shadow-lg rounded-lg w-full max-w-2xl mx-auto flex flex-col gap-6"
      style={{ padding: "30px", marginBottom: "30px" }}
    >
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        📊 Research Summary
      </h2>

      <div className="mb-2">
        <strong className="text-gray-700">🏷️ Value Proposition:</strong>
        <p className="text-gray-600">{result.company_value_prop}</p>
      </div>

      <div className="mb-2">
        <strong className="text-gray-700">🧩 Products:</strong>
        <p className="text-gray-600">{result.product_names.join(", ")}</p>
      </div>

      <div className="mb-2">
        <strong className="text-gray-700">💰 Pricing Model:</strong>
        <p className="text-gray-600">{result.pricing_model}</p>
      </div>

      <div className="mb-2">
        <strong className="text-gray-700">🏁 Competitors:</strong>
        <p className="text-gray-600">{result.key_competitors.join(", ")}</p>
      </div>

      <div className="mb-2">
        <strong className="text-gray-700">🌐 Company Domain:</strong>
        <p className="text-blue-600">{result.company_domain}</p>
      </div>

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
