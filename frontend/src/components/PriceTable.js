import React from "react";

const PriceTable = ({ terms, prices, term, coverage, labels, coverages }) => {
  return (
    <table>
      <th></th>
      {terms.map((t) => (
        <th>{t}</th>
      ))}
      {prices.map((price) => {
        return (
          <tr>
            <th>{labels[coverages.indexOf(price["coverage"])]}</th>
            {terms.map((t) =>
              Number(t) === Number(term) &&
              Number(price["coverage"]) === Number(coverage) ? (
                <td>
                  <b>{price[t]}</b>
                </td>
              ) : <td>{price[t]}</td>
            )}
          </tr>
        );
      })}
    </table>
  );
};

export default PriceTable;
