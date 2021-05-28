import React, { Fragment, useEffect, useState } from "react";
import { withRouter } from "react-router-dom";
import { PriceTable, Options } from "../../components";

const TERMS = [10, 15, 20, 25, 30];
const COVERAGES = [100000, 250000, 500000, 1000000, 5000000, 10000000];
const LABELS = ["100K", "250K", "500K", "1M", "5M", "10M"];

const DisplayPrices = () => {
  const [displayTerms, setDisplayTerms] = useState([]);
  const [term, setTerm] = useState("");
  const [coverage, setCoverage] = useState("");
  const [prices, setPrices] = useState([]);

  const handleSelectedTerm = (evt) => {
    setTerm(evt.target.value);
  };

  const handleSelectedCoverage = (evt) => {
    setCoverage(evt.target.value);
  };

  useEffect(() => {
    if (term && coverage) {
      fetch(`/api/prices?term=${term}&coverage_amount=${coverage}`)
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          return data;
        })
        .then((data) => {
          setDisplayTerms(data.terms);
          setPrices(data.prices);
        });
    }
  }, [term, coverage]);

  return (
    <Fragment>
      <div className="container">
        <h2>Select Term:</h2>
        <select value={term} onChange={handleSelectedTerm}>
          <Options options={TERMS} disabledLabel="Years" />
        </select>
        <p>{term ? `Selected Term: ${term} YEARS` : ""}</p>
      </div>

      <div className="container">
        <h2>Select Coverage Amount:</h2>
        <select value={coverage} onChange={handleSelectedCoverage}>
          <Options options={COVERAGES} disabledLabel="US Dollars" />
        </select>
        <p>
          {coverage ? `Selected Coverage Amount: $${Number(coverage).toLocaleString("en-US")}` : ""}
        </p>
      </div>

      <div className="container">
        {term && coverage ?
          <PriceTable
            terms={displayTerms}
            prices={prices}
            term={term}
            coverage={coverage}
            labels={LABELS}
            coverages={COVERAGES}
          /> : ""}
      </div>
    </Fragment>
  );
};

export default withRouter(DisplayPrices);
