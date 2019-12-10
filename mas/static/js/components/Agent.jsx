import React from "react";
import axios from "axios";

import ClipLoader from "react-spinners/ClipLoader";

export default class Agent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
      keywords: "",
      data: []
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({
      keywords: event.target.value
    });
  }

  handleSubmit(event) {
    this.setState({
      isLoading: true
    });

    axios
      .post("/agent/search", {
        keywords: this.state.keywords
      })
      .then(response => {
        console.log(response.data);
        console.log(response.data[0])
        this.setState({
          data: response.data,
          isLoading: false
        });
      });

    event.preventDefault();
  }

  render() {
    let urls =
      this.state.data.length != 0
        ? this.state.data.select(function(x) {
            return x.vacancies.length === 0;
          })
        : [];

    let otherUrls = urls.map((item, key) => (
      <a href={item.url} class="list-group-item list-group-item-action">
        {item.name}
      </a>
    ));

    let content =
      this.state.isLoading == true ? (
        <ClipLoader
          sizeUnit={"px"}
          size={150}
          color={"#123abc"}
          loading={this.state.isLoading}
        />
      ) : null;

    let card = (
      <div class="card w-25 p-3">
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
          <p class="card-text">
            Some quick example text to build on the card title and make up the
            bulk of the card's content.
          </p>
          <a href="#" class="card-link">
            Card link
          </a>
        </div>
      </div>
    );

    return (
      <div id="agent" class="container py-5">
        <div class="row">
          <div class="col-md-4 mx-auto">
            <div class="row">
              <div class="col-md-12 mx-auto">
                <h4 class="mb-3 text-center">Vacancy Search Agent</h4>
                <p class="mb-3 text-center">
                  Details about your vacancy?
                </p>
                <form
                  class="needs-validation"
                  novalidate=""
                  onSubmit={this.handleSubmit}
                >
                  <div class="mb-3">
                    <div class="input-group">
                      <input
                        type="text"
                        class="form-control"
                        id="keywords"
                        placeholder="Keywords for vacancy"
                        required=""
                        value={this.state.keywords}
                        onChange={this.handleChange}
                      />
                      <div class="invalid-feedback">
                        Request keywords are required.
                      </div>
                    </div>
                  </div>

                  <hr class="mb-4" />
                  <button
                    class="btn btn-primary btn-lg btn-block"
                    type="submit"
                  >
                    Search
                  </button>
                </form>
              </div>
            </div>
            <div class="row py-1">
              <div class="col-md-12 mx-auto">
                <div class="list-group list-group-flush">{otherUrls}</div>
              </div>
            </div>
          </div>

          <div class="col-md-8 mx-auto center-block">{content}</div>
        </div>
      </div>
    );
  }
}
