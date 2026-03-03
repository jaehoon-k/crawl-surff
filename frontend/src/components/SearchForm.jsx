import { useState } from 'react';

const SearchForm = ({ onSearch, isLoading }) => {
    const [cntrType, setCntrType] = useState("40 Dry");
    const [pol, setPol] = useState("KRPUS(BUSAN)");
    const [pod, setPod] = useState("USBOS");
    const [period, setPeriod] = useState("6개월");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!cntrType || !pol || !pod || !period) return;
        onSearch({ cntr_type: cntrType, pol, pod, period });
    };

    return (
        <form className="search-form" onSubmit={handleSubmit}>
            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="cntrType">Container Type & Size</label>
                    <select
                        id="cntrType"
                        className="form-control"
                        value={cntrType}
                        onChange={(e) => setCntrType(e.target.value)}
                        disabled={isLoading}
                    >
                        <option value="40 Dry">40' Dry</option>
                        <option value="20 Dry">20' Dry</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="pol">Port of Loading (POL)</label>
                    <input
                        type="text"
                        id="pol"
                        className="form-control"
                        value={pol}
                        onChange={(e) => setPol(e.target.value.toUpperCase())}
                        placeholder="e.g. KRPUS"
                        disabled={isLoading}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="pod">Port of Discharge (POD)</label>
                    <input
                        type="text"
                        id="pod"
                        className="form-control"
                        value={pod}
                        onChange={(e) => setPod(e.target.value.toUpperCase())}
                        placeholder="e.g. USBOS"
                        disabled={isLoading}
                        required
                    />
                </div>
            </div>

            <div className="form-row" style={{ marginTop: '0.5rem' }}>
                <div className="form-group">
                    <label htmlFor="period">Query Period</label>
                    <select
                        id="period"
                        className="form-control"
                        value={period}
                        onChange={(e) => setPeriod(e.target.value)}
                        disabled={isLoading}
                    >
                        <option value="1개월">1 Month (1개월)</option>
                        <option value="3개월">3 Months (3개월)</option>
                        <option value="6개월">6 Months (6개월)</option>
                        <option value="1년">1 Year (1년)</option>
                        <option value="전체">All (전체)</option>
                    </select>
                </div>
            </div>

            <button
                type="submit"
                className="btn-primary"
                disabled={isLoading || !pol || !pod}
            >
                {isLoading ? (
                    <>
                        <span className="loader"></span>
                        Crawling Fares...
                    </>
                ) : (
                    'Search Real-time Fares'
                )}
            </button>
        </form>
    );
};

export default SearchForm;
