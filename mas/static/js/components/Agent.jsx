import React from "react";
import axios from "axios";
import styled, { keyframes } from "styled-components";
import ZoomInUp from "react-animations";
import ClipLoader from "react-spinners/ClipLoader";

const ZoomInUpAnimation = keyframes`${ZoomInUp}`;
const ZoomInUpDiv = styled.div`
  animation: infinite 10s ${ZoomInUpAnimation};
`;

function getLoader(loading) {
  return (
    <div class="d-flex h-100 justify-content-center align-items-center">
      <ClipLoader
        sizeUnit={"px"}
        size={150}
        color={"#123abc"}
        loading={loading}
      />
    </div>
  );
}

function getErrorMessage() {
  return (
    <div class="d-flex h-100 justify-content-center align-items-center">
      <div class="alert alert-danger" role="alert">
        Произошла ошибка во время выполнения запроса. Пожалуйста, повторите Ваш
        запрос.
      </div>
    </div>
  );
}

function getInitialMessage() {
  return (
    <div class="d-flex h-100 justify-content-center align-items-center">
      <div class="alert alert-primary" role="alert">
        Введите критерии вакансии и нажмите кнопку "Создать запрос"
      </div>
    </div>
  );
}

function getHostnameFromUrl(url) {
  var element = document.createElement("a");
  element.href = url;
  return element.hostname;
}

export default class Agent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
      isLoadingErrorHandled: false,
      position: "",
      salary: 0,
      county: "",
      city: "",
      withoutExperience: false,

      data: []
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.getUrlsList = this.getUrlsList.bind(this);
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
    console.log("Request...");
    this.setState({
      isLoadingErrorHandled: false,
      isLoading: true,
      data: []
    });

    axios
      .post(
        "/agent/search",
        {
          position: this.state.position,
          keywords: this.state.keywords,
          salary: this.state.salary,
          country: this.state.county,
          city: this.state.city
        },
        { timeout: 40000 }
      )
      .then(response => {
        console.log("Request accepted. Response ->");
        console.log(response.data);
        this.setState({
          data: response.data,
          isLoadingErrorHandled: false,
          isLoading: false
        });
      })
      .catch(ex => {
        console.log("Request aborted. Exception ->");
        console.error(ex);
        this.setState({
          isLoadingErrorHandled: true,
          isLoading: false
        });
      });

    event.preventDefault();
  }

  getCardsList(data, type) {
    let content = data.map(url =>
      url["vacancies"].map(item =>
        type == item["type"] ? (
          <ZoomInUpDiv>
            <a href={item["link"]}>
              <div class="card">
                <div class="card-body">
                  <img class="card-img-top" src={item["image"]} />
                  <h5 class="card-title vac-name">{item["name"]}</h5>
                  <h6 class="card-subtitle mb-2 font-weight-bold">
                    {item["salary"]}
                  </h6>
                  <h6 class="card-subtitle mb-2 text-muted">
                    {item["company"]}
                    {item["location"] ? " - " + item["location"] : null}
                  </h6>
                  <p class="card-text">{item["description"]}</p>
                </div>
              </div>
            </a>
          </ZoomInUpDiv>
        ) : null
      )
    );

    return <div class="card-columns">{content}</div>;
  }

  getUrlsList(data) {
    console.log("Urls list ->");
    console.log(data);
    let content = data.map(item => (
      <li class="list-group-item d-flex justify-content-between lh-condensed">
        <a href={item["url"]}>
          <h6 class="my-0">
            {item["name"] ? item["name"] : getHostnameFromUrl(item["domain"])}
          </h6>
          <small class="text-muted text-wrap">{item["title"]}</small>
        </a>
      </li>
    ));

    return (
      <div class="overflow-auto" id="urls-list">
        <ul class="list-group mb-3">{content}</ul>
      </div>
    );
  }

  render() {
    let vacanciesMain = this.getCardsList(
      this.state.data.filter(item => item["vacancies"].length > 0),
      "main"
    );

    let vacanciesRelated = this.getCardsList(
      this.state.data.filter(item => item["vacancies"].length > 0),
      "related"
    );

    let content = this.state.isLoading ? (
      getLoader(this.state.isLoading)
    ) : this.state.isLoadingErrorHandled ? (
      getErrorMessage()
    ) : this.state.data.length > 0 ? (
      <div>
        {vacanciesMain}
        {vacanciesRelated.length > 0 ? (
          <div>
            <hr class="mb-4" />
            <h4 class="mb-3 text-center">Дополнительные вакансии</h4>
            {vacanciesRelated}
          </div>
        ) : null}
      </div>
    ) : (
      getInitialMessage()
    );

    let urls =
      this.state.data.length > 0 ? (
        <div>
          {this.getUrlsList(
            this.state.data.filter(item => item["vacancies"].length === 0)
          )}
        </div>
      ) : null;

    return (
      <div id="agent" class="container py-5">
        <div class="row">
          <div class="col-md-4 mx-auto">
            <div class="row">
              <div class="col-md-12 mx-auto">
                <h4 class="mb-3">Критерии запроса</h4>
                <form
                  class="needs-validation"
                  onSubmit={this.handleSubmit}
                  noValidate
                >
                  <div class="mb-3">
                    <label for="position">Должность</label>
                    <div class="input-group">
                      <input
                        type="text"
                        class="form-control"
                        id="position"
                        placeholder="Хочу работать"
                        required
                        value={this.state.position}
                        onChange={this.handleChange}
                      />
                      <div class="invalid-feedback">
                        Должность не может быть пустой
                      </div>
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="salary">Заработная плата от ... (USD)</label>
                    <input
                      type="text"
                      class="form-control"
                      id="salary"
                      placeholder="0"
                      value={this.state.salary}
                      onChange={this.handleChange}
                    />
                  </div>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="country">Страна</label>
                      <select
                        class="custom-select d-block w-100"
                        id="country"
                        required
                        value={this.state.country}
                        onChange={this.handleChange}
                      >
                        <option>Беларусь</option>
                      </select>
                      <div class="invalid-feedback">
                        Пожалуйста, введите реальное название страны.
                      </div>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label for="city">Город</label>
                      <select
                        class="custom-select d-block w-100"
                        id="city"
                        value={this.state.city}
                        onChange={this.handleChange}
                      >
                        <option>Гродно</option>
                      </select>
                      <div class="invalid-feedback">
                        Пожалуйста, введите реальное название города.
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
                      Без опыта работы
                    </label>
                  </div>

                  <hr class="mb-4" />
                  <button
                    class="btn btn-primary btn-lg btn-block w-75 m-auto"
                    type="submit"
                    disabled={this.state.isLoading}
                  >
                    {this.state.isLoading
                      ? "Запрос обрабатывается..."
                      : "Создать запрос"}
                  </button>
                </form>
              </div>
            </div>
            <div class="row py-1">
              <div class="col-md-12 mx-auto">{urls}</div>
            </div>
          </div>

          <div class="col-md-8 mx-auto center-block">{content}</div>
        </div>
      </div>
    );
  }
}
