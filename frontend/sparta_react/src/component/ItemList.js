import {Link} from "react-router-dom";
import {Container, Row, Col} from 'react-bootstrap';
import {useState} from "react";
import axios from 'axios';

export default function ItemList() {
    const [keyword, setKeyword] = useState('');
    const [datas, setDatas] = useState([]);


    function register() {

    }

    function search() {
        const url = `http://127.0.0.1:8000/api/v1/items/?keyword=${keyword}`
        fetch(url)
            .then(res => {
                return res.json()
            })
            .then(data => {
                setDatas(data);
            })
    }

    function handle_KeywordTextChange(e) {
        setKeyword(e.target.value)
    }

    return (
        <>
            <div>h1</div>
            <div>h1</div>
            <div>h1</div>
            <Container className="">
                <Row>
                    <Col>
                        <select name="category" className="form-select" aria-label="">
                            <option value="title">제목
                            </option>
                            <option value="username" selected>작성자
                            </option>
                            <option value="content" selected>내용
                            </option>
                        </select>
                    </Col>
                    <Col>
                        <input type="text" name="keyword" className="form-control w-100" onChange={handle_KeywordTextChange}/>
                    </Col>
                    <Col>
                        <button className="btn btn-danger" onClick={search}>검색</button>
                    </Col>
                </Row>
            </Container>
            <ul>
                {datas.map(data => (
                    <li key={data.id}>
                        {data.title}
                        {/*<Link to={`/day/${day.day}`}>title:{day.title} {day.day}</Link>*/}
                    </li>
                ))}
            </ul>
        </>

    );
}