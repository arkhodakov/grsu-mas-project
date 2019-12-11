import React from "react";
import axios from "axios";

import ClipLoader from "react-spinners/ClipLoader";

export default class Agent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
      position: "",
      keywords: "",
      salary: 0,
      county: "",
      city: "",
      withoutExperience: false,

      data: []
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.id;

    this.setState({
      [name]: value
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
        console.log(response.data[0]);
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
        <div class="d-flex h-100 justify-content-center align-items-center">
          <ClipLoader
            sizeUnit={"px"}
            size={150}
            color={"#123abc"}
            loading={this.state.isLoading}
          />
        </div>
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
                <h4 class="mb-3">Vacancy parameters</h4>
                <form
                  class="needs-validation"
                  onSubmit={this.handleSubmit}
                  noValidate
                >
                  <div class="mb-3">
                    <label for="position">Position</label>
                    <div class="input-group">
                      <div class="input-group-prepend">
                        <span class="input-group-text">I'm a</span>
                      </div>
                      <input
                        type="text"
                        class="form-control"
                        id="position"
                        placeholder="Position"
                        required
                        value={this.state.position}
                        onChange={this.handleChange}
                      />
                      <div class="invalid-feedback">Position is required</div>
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="salary">Minimum salary</label>
                    <input
                      type="text"
                      class="form-control"
                      id="salary"
                      placeholder="0"
                      value={this.state.salary}
                      onChange={this.handleChange}
                    />
                  </div>

                  <div class="mb-3">
                    <label for="keywords">Keywords</label>
                    <input
                      type="text"
                      class="form-control"
                      id="keywords"
                      placeholder="Keywords about vacancy"
                      value={this.state.keywords}
                      onChange={this.handleChange}
                    />
                    <small class="text-muted">
                      It can be technologies, tools, skills
                    </small>
                  </div>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="country">Country</label>
                      <select
                        class="custom-select d-block w-100"
                        id="country"
                        required
                        value={this.state.country}
                        onChange={this.handleChange}
                      >
                        <option value="Belarus">Belarus</option>
                      </select>
                      <div class="invalid-feedback">
                        Please select a valid country.
                      </div>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="city">City</label>
                      <select
                        class="custom-select d-block w-100"
                        id="city"
                        value={this.state.city}
                        onChange={this.handleChange}
                      >
                        <option value="Hrodno">Hrodno</option>
                      </select>
                      <div class="invalid-feedback">
                        Please provide a valid city.
                      </div>
                    </div>
                  </div>

                  <hr class="mb-4" />
                  <div class="custom-control custom-checkbox">
                    <input
                      type="checkbox"
                      class="custom-control-input"
                      id="withoutExperience"
                      value={this.state.withoutExperience}
                      onChange={this.handleChange}
                    />
                    <label class="custom-control-label" for="withoutExperience">
                      No work experience
                    </label>
                  </div>

                  <hr class="mb-4" />
                  <button
                    class="btn btn-primary btn-lg btn-block"
                    type="submit"
                    disabled={this.state.isLoading}
                  >
                    {this.state.isLoading ? "Searching..." : "Search"}
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
