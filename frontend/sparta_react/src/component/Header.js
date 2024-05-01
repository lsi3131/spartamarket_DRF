import {Link} from "react-router-dom";

export default function Header() {
    return (
        <div>
            <nav className="nav-bar">
                <div className="nav-container">
                    <Link className="" to="/">
                        <img className="navbar-image-logo" src="/images/sparta.png" alt=""/>
                        <span>스파르타마켓</span>
                    </Link>

                    <div>
                        <Link to="profile" className="nav-btn">내정보</Link>
                        <Link to="like_list" className="nav-btn">관심 목록</Link>
                        <Link to="register_item_list" className="nav-btn">등록 제품</Link>
                        <Link to="logout" className="nav-btn">로그 아웃</Link>
                        <Link to="login" className="nav-btn">로그인</Link>
                    </div>
                </div>
            </nav>
        </div>
    );
}